import json
import logging
import re
import time
from typing import Dict, Any, List, Optional
from google import genai
from google.genai import types
from app.config import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT_EN = """You are KaamSaathi AI (कामसाथी), an empathetic, practical, and trustworthy AI companion for gig and informal workers in India (such as food delivery partners, cab drivers, auto drivers, and daily-wage construction workers).

Core Guidelines:
1. Simplicity & Clarity: Use plain, everyday language, short sentences, and bullet points. Avoid legal jargon or complex financial terms.
2. Grounded & Honest: Never hallucinate numbers, dates, legal conclusions, or eligibility decisions. If information is missing or uncertain, explicitly state it.
3. Safety: For emergencies or violence, prioritize immediate safety, emergency helplines (112, 108), and physical withdrawal over app advice.
4. Worker Empowerment: Explain worker rights respectfully without overpromising legal outcomes.
"""

SYSTEM_PROMPT_HI = """आप 'कामसाथी AI' हैं - भारत के गिग और असंगठित क्षेत्र के कामगारों (जैसे डिलीवरी पार्टनर, कैब/ऑटो चालक, दिहाड़ी व निर्माण मजदूर) के सच्चे, सरल और मददगार डिजिटल साथी।

मुख्य दिशानिर्देश:
1. सरल भाषा: एकदम आसान हिंदी या रोज़मर्रा की व्यावहारिक भाषा (हिंग्लिश) का प्रयोग करें। छोटे-छोटे वाक्यों और बुलेट पॉइंट्स में समझाएं।
2. प्रमाणिकता: किसी भी नियम, आंकड़े, तारीख या कानूनी अधिकार के बारे में झूठा या बनावटी दावा न करें। यदि जानकारी उपलब्ध नहीं है, तो साफ बताएं।
3. सुरक्षा सर्वोपरि: किसी भी खतरे, दुर्घटना या आपातकाल में तुरंत 112 या 108 पर कॉल करने और खुद को सुरक्षित रखने की सलाह दें।
4. कामगार सम्मान: कामगार के अधिकारों और स्वाभिमान का पूरा सम्मान करते हुए व्यावहारिक कदम बताएं।
"""

class AIServiceError(Exception):
    """Explicit exception raised when AI service call fails or credentials are missing."""
    def __init__(self, status_code: int, message: str):
        super().__init__(message)
        self.status_code = status_code
        self.message = message

# In-memory record of the last explicit connection test
# Distinguishes between configured key and verified live availability
_last_verification_state: Dict[str, Any] = {
    "verified": False,
    "last_tested_at": None,
    "latency_ms": None,
    "message": None,
    "error": None
}

def get_verification_status() -> Dict[str, Any]:
    """Returns the cached verification result of the last explicit test without making a network call."""
    return dict(_last_verification_state)

def get_client() -> genai.Client:
    api_key = settings.get_api_key()
    if not api_key:
        raise AIServiceError(
            status_code=503,
            message="Gemini API key is not configured. Please set the GEMINI_API_KEY environment variable on the server."
        )
    try:
        http_options = types.HttpOptions(timeout=settings.AI_TIMEOUT_MS)
        return genai.Client(api_key=api_key, http_options=http_options)
    except Exception as e:
        logger.error(f"Failed to initialize GenAI Client: {e}")
        raise AIServiceError(
            status_code=502,
            message=f"Failed to initialize Gemini AI client: {str(e)}"
        )

def is_api_configured() -> bool:
    return bool(settings.get_api_key())

def test_ai_connection() -> Dict[str, Any]:
    """Makes a genuine model call to verify live availability of gemini-3.8-flash."""
    if not is_api_configured():
        res = {
            "verified": False,
            "model": settings.GEMINI_MODEL,
            "error": "GEMINI_API_KEY environment variable is not configured."
        }
        _last_verification_state.update({
            "verified": False,
            "last_tested_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "latency_ms": None,
            "error": res["error"]
        })
        return res

    try:
        client = get_client()
        start = time.time()
        resp = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents="Respond with the single word: OK",
            config=types.GenerateContentConfig(max_output_tokens=10)
        )
        latency = round((time.time() - start) * 1000)
        text = resp.text.strip() if resp and resp.text else ""
        res = {
            "verified": True,
            "model": settings.GEMINI_MODEL,
            "latency_ms": latency,
            "message": f"Successfully verified live connection to {settings.GEMINI_MODEL}."
        }
        _last_verification_state.update({
            "verified": True,
            "last_tested_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "latency_ms": latency,
            "message": res["message"],
            "error": None
        })
        return res
    except Exception as e:
        logger.error(f"AI test connection failed: {e}")
        err_msg = f"Model connection test failed: {str(e)}"
        _last_verification_state.update({
            "verified": False,
            "last_tested_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "latency_ms": None,
            "error": err_msg
        })
        return {
            "verified": False,
            "model": settings.GEMINI_MODEL,
            "error": err_msg
        }

def _clean_json_text(raw_text: str) -> str:
    """Strips markdown code fences and cleans json response."""
    text = raw_text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.MULTILINE)
        text = re.sub(r"```\s*$", "", text, flags=re.MULTILINE)
    return text.strip()

def generate_chat_reply(
    message: str,
    session_id: str = "default",
    language: str = "en",
    context_type: Optional[str] = None,
    context_data: Optional[Dict[str, Any]] = None,
    history: Optional[List[Dict[str, str]]] = None
) -> Dict[str, Any]:
    """Generates an AI chat reply with context grounding and routing detection using gemini-3.8-flash."""
    msg_lower = message.lower()
    routing_target = None
    suggested_actions = []

    if any(k in msg_lower for k in ["earning", "income", "kamaee", "kamai", "hisab", "kharcha", "expense", "calculate"]):
        routing_target = "earnings"
        suggested_actions.append({"text": "📊 Open Earnings Tracker", "action": "navigate_earnings"})
    elif any(k in msg_lower for k in ["safety", "suraksha", "accident", "threat", "police", "danger", "customer fight"]):
        routing_target = "safety"
        suggested_actions.append({"text": "🛡️ View Safety Checklists", "action": "navigate_safety"})
    elif any(k in msg_lower for k in ["scheme", "yojana", "eshram", "pension", "bocw", "ayushman", "योजना", "ई-श्रम"]):
        routing_target = "welfare"
        suggested_actions.append({"text": "🏛️ Browse Welfare Schemes", "action": "navigate_welfare"})
    elif any(k in msg_lower for k in ["contract", "agreement", "document", "slip", "kagaz", "pdf", "statement"]):
        routing_target = "document"
        suggested_actions.append({"text": "📄 Analyze a Document", "action": "navigate_document"})
    elif any(k in msg_lower for k in ["dispute", "complaint", "shikayat", "unpaid", "deduction", "suspended", "penalty"]):
        routing_target = "grievance"
        suggested_actions.append({"text": "⚖️ Draft Formal Grievance", "action": "navigate_grievance"})

    if not is_api_configured():
        raise AIServiceError(
            status_code=503,
            message="Gemini API key is not configured on the server. Please set the GEMINI_API_KEY environment variable."
        )

    client = get_client()

    # Build prompt context
    system_instruction = SYSTEM_PROMPT_HI if language.startswith("hi") else SYSTEM_PROMPT_EN
    context_str = ""
    if context_data:
        context_str = f"\n[RELEVANT WORKER DATA CONTEXT provided by application]:\n{json.dumps(context_data, indent=2)}\n"

    prompt = f"""Language instruction: Reply in {'simple, polite Hindi (Devanagari script)' if language.startswith('hi') else 'simple, clear English'}.
{context_str}
Worker Question: "{message}"

Provide a direct, practical, empathetic response with short bullet points where actionable. If relevant, remind them to check their local safety or rights."""

    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        )
        if not response or not response.text:
            raise AIServiceError(502, "AI model returned an empty response.")
        return {
            "reply": response.text.strip(),
            "language": language,
            "suggested_actions": suggested_actions,
            "routing_target": routing_target
        }
    except AIServiceError:
        raise
    except Exception as e:
        logger.error(f"Gemini API chat error on {settings.GEMINI_MODEL}: {e}")
        # Return a safe, sanitized error message without leaking sensitive internal diagnostics
        raise AIServiceError(502, "AI chat service is temporarily unavailable. Please try again.")

def explain_earnings(summary_data: Dict[str, Any], recent_entries: List[Dict[str, Any]], language: str = "en") -> str:
    """Explains actual recorded earnings, expense ratios, and practical savings using gemini-3.8-flash."""
    client = get_client()

    prompt = f"""You are KaamSaathi AI analyzing actual recorded financial records for an informal or gig worker in India.
Language: {'Hindi' if language.startswith('hi') else 'English'}.

Actual Recorded Earnings Summary:
- Today Net: ₹{summary_data.get('today', {}).get('total_net', 0)} (Gross: ₹{summary_data.get('today', {}).get('total_gross', 0)}, Expenses: ₹{summary_data.get('today', {}).get('total_expenses', 0)})
- Last 7 Days Net: ₹{summary_data.get('this_week', {}).get('total_net', 0)} (Gross: ₹{summary_data.get('this_week', {}).get('total_gross', 0)}, Expenses: ₹{summary_data.get('this_week', {}).get('total_expenses', 0)})
- This Month Net: ₹{summary_data.get('this_month', {}).get('total_net', 0)} (Gross: ₹{summary_data.get('this_month', {}).get('total_gross', 0)}, Expenses: ₹{summary_data.get('this_month', {}).get('total_expenses', 0)})
- All-time Net: ₹{summary_data.get('all_time', {}).get('total_net', 0)}

Recent actual entries (up to 5):
{json.dumps(recent_entries[:5], indent=2)}

Task:
1. Explain the worker's net take-home earnings clearly.
2. Highlight their expense-to-gross ratio (e.g. fuel, commission).
3. Offer 2 short, practical tips to manage expenses or plan peak earning hours.
4. Keep the tone encouraging and honest based strictly on these figures. Do not fabricate extra numbers."""

    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT_HI if language.startswith("hi") else SYSTEM_PROMPT_EN
            )
        )
        if not response or not response.text:
            raise AIServiceError(502, "Gemini returned an empty explanation.")
        return response.text.strip()
    except AIServiceError:
        raise
    except Exception as e:
        logger.error(f"Gemini explain_earnings error on {settings.GEMINI_MODEL}: {e}")
        raise AIServiceError(502, "Failed to generate earnings explanation from AI. Please try again.")

def _ensure_document_mandatory_items(data: Dict[str, Any], doc_type: str = "General Document", language: str = "en") -> None:
    """Guarantees at least 1-2 items for mandatory document sections (questions_to_ask and missing_info_checklist)."""
    is_hi = language.startswith("hi")
    doc_lower = (doc_type or "").lower()

    # Guarantee 1-2 items for questions_to_ask
    questions = data.get("questions_to_ask")
    if not isinstance(questions, list) or len(questions) == 0:
        if any(term in doc_lower for term in ["payment", "statement", "salary", "payout", "slip"]):
            data["questions_to_ask"] = [
                "मेरे बैग/टी-शर्ट कटौती की कितनी किस्तें बची हैं?" if is_hi else "How many installments are left for my bag deduction?",
                "क्या आप प्लेटफॉर्म एक्सेस फीस और कटौती की गणना का आधार बता सकते हैं?" if is_hi else "Can you provide the calculation basis for the platform access fee?"
            ]
        else:
            data["questions_to_ask"] = [
                "विवाद या कटौती संबंधी समस्या होने पर सपोर्ट से संपर्क करने की आधिकारिक समय-सीमा क्या है?" if is_hi else "What is the official support dispute resolution window for these clauses?",
                "क्या इस नियम या कटौती का कोई स्पष्ट लिखित ब्रेकडाउन प्रदान किया जा सकता है?" if is_hi else "Can support provide a detailed written calculation breakdown for this?"
            ]
    elif len(questions) == 1:
        if any(term in doc_lower for term in ["payment", "statement", "salary", "payout", "slip"]):
            supp = "क्या आप प्लेटफॉर्म एक्सेस फीस और कटौती की गणना का आधार बता सकते हैं?" if is_hi else "Can you provide the calculation basis for the platform access fee?"
            if questions[0] != supp:
                questions.append(supp)

    # Guarantee 1-2 items for missing_info_checklist
    missing = data.get("missing_info_checklist")
    if not isinstance(missing, list) or len(missing) == 0:
        if is_hi:
            data["missing_info_checklist"] = [
                "कटौती, पेनल्टी और विवाद समाधान की स्पष्ट समय-सीमा का उल्लेख नहीं है",
                "शिकायत निवारण अधिकारी और अपील प्रक्रिया का आधिकारिक विवरण अनुपस्थित है"
            ]
        else:
            data["missing_info_checklist"] = [
                "Missing clear dispute resolution timeline and appeal process",
                "Unstated calculation formulas for platform fees or deductions"
            ]

def analyze_document_text(text: str, doc_type: str = "General Document", language: str = "en") -> Dict[str, Any]:
    """Analyzes text extracted from a contract, payment statement, or notice using gemini-3.8-flash."""
    client = get_client()

    base_prompt = f"""You are KaamSaathi AI analyzing a work-related document for a gig or informal worker.
Language of Output: {'Hindi' if language.startswith('hi') else 'English'}.
Document Type: {doc_type}

Actual Document Text:
\"\"\"
{text[:12000]}
\"\"\"

Strict Grounding Rules:
- Extract ONLY what is stated in the document text above.
- Do NOT invent clauses, rates, or obligations not present.
- Mandatory Section Requirements:
  * Always output at least one recommended question the worker should ask support based on the document (always generate 1-2 items for 'questions_to_ask'). For payment statements, suggest questions like 'How many installments are left for my bag deduction?' or 'Can you provide the calculation basis for the platform access fee?'.
  * Always output 1-2 items for 'missing_info_checklist' identifying missing details, unstated dispute windows, vague deduction rules, or absent signatures.
- Return valid JSON matching the exact schema below:

{{
  "summary": "2-3 sentences plain language summary explaining what this document is and its main impact on the worker.",
  "key_amounts": ["List of amounts, incentives, penalties, or wages explicitly mentioned"],
  "important_dates": ["List of effective dates, payment dates, or dispute notice windows mentioned"],
  "conditions_and_clauses": ["List of critical obligations or deduction rules stated"],
  "missing_info_checklist": ["Always 1-2 items: List of missing details, unstated dispute deadlines, or clarity gaps"],
  "questions_to_ask": ["Always 1-2 items: Recommended questions the worker should ask support based on the document. For payment statements, suggest questions like 'How many installments are left for my bag deduction?' or 'Can you provide the calculation basis for the platform access fee?'"],
  "disclaimer": "This analysis provides plain-language informational assistance based solely on the provided text. It does not constitute formal legal counsel."
}}
"""

    def call_model(p: str) -> str:
        resp = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=p,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        if not resp or not resp.text:
            raise AIServiceError(502, "AI model returned an empty response.")
        return resp.text.strip()

    try:
        raw = call_model(base_prompt)
        cleaned = _clean_json_text(raw)
        result = json.loads(cleaned)
        _ensure_document_mandatory_items(result, doc_type=doc_type, language=language)
        return result
    except (json.JSONDecodeError, ValueError) as json_err:
        logger.warning(f"Initial JSON parse failed: {json_err}. Retrying once with strict JSON prompt...")
        retry_prompt = base_prompt + "\n\nCRITICAL: Output ONLY valid, parseable JSON. Ensure 'questions_to_ask' and 'missing_info_checklist' each contain 1-2 items."
        try:
            raw_retry = call_model(retry_prompt)
            cleaned_retry = _clean_json_text(raw_retry)
            result = json.loads(cleaned_retry)
            _ensure_document_mandatory_items(result, doc_type=doc_type, language=language)
            return result
        except Exception as retry_err:
            logger.error(f"JSON parsing retry also failed: {retry_err}")
            raise AIServiceError(502, "AI service returned an unparseable response format. Please try again.")
    except AIServiceError:
        raise
    except Exception as e:
        logger.error(f"Doc analysis error on {settings.GEMINI_MODEL}: {e}")
        raise AIServiceError(502, "Failed to analyze document with AI. Please try again.")

def draft_grievance_dispute(
    category: str,
    employer_platform: str,
    incident_date: str,
    amount_disputed: Optional[float],
    incident_details: str,
    evidence_available: Optional[str],
    language: str = "en",
    linked_earning: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Generates a structured, respectful, and firm grievance letter based strictly on provided facts using gemini-3.8-flash."""
    client = get_client()

    earning_context = ""
    if linked_earning:
        earning_context = f"\nReferenced App Earnings Record:\n- Date: {linked_earning.get('date')}\n- Gross: ₹{linked_earning.get('gross_earnings')}\n- Recorded Net: ₹{linked_earning.get('net_earnings')}\n- Notes: {linked_earning.get('notes')}\n"

    base_prompt = f"""You are KaamSaathi AI assisting a worker to draft a professional, respectful, concise formal complaint or dispute notice to their employer or aggregator platform.
Language: {'Hindi' if language.startswith('hi') else 'English'}.

Grievance Facts Supplied by Worker:
- Issue Category: {category}
- Platform/Employer: {employer_platform}
- Date of Incident: {incident_date}
- Amount Disputed: {'₹' + str(amount_disputed) if amount_disputed is not None else 'Not specified / Non-monetary'}
- Description of Incident: {incident_details}
- Evidence Worker Holds: {evidence_available or 'None specified'}
{earning_context}

Requirements:
1. Provide a professional Subject Line and a well-structured message body with clear paragraphs:
   - Salutation to Platform Support / Grievance Officer
   - Clear statement of the issue with date, ID or order references
   - Specific resolution or correction requested
   - Reiteration of worker cooperation and contact readiness
2. Use respectful, calm, yet firm language. Do NOT fabricate facts, dates, or ticket numbers. If a detail like Order ID is not provided, write '[Insert Order/Trip ID here]' in brackets.
3. Return valid JSON matching:
{{
  "generated_draft": "The full complete text of the email/letter ready to copy",
  "checklist": ["3-4 supporting proofs or documents the worker should attach"],
  "next_steps": ["3 actionable steps for the worker after sending this message"]
}}
"""

    def call_model(p: str) -> str:
        resp = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=p,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        if not resp or not resp.text:
            raise AIServiceError(502, "AI model returned an empty response.")
        return resp.text.strip()

    try:
        raw = call_model(base_prompt)
        cleaned = _clean_json_text(raw)
        return json.loads(cleaned)
    except (json.JSONDecodeError, ValueError) as json_err:
        logger.warning(f"Initial grievance JSON parse failed: {json_err}. Retrying once...")
        retry_prompt = base_prompt + "\n\nCRITICAL: Return ONLY valid, parseable JSON with keys 'generated_draft', 'checklist', and 'next_steps'."
        try:
            raw_retry = call_model(retry_prompt)
            cleaned_retry = _clean_json_text(raw_retry)
            return json.loads(cleaned_retry)
        except Exception as retry_err:
            logger.error(f"Grievance JSON parsing retry failed: {retry_err}")
            raise AIServiceError(502, "AI service returned an unparseable response format. Please try again.")
    except AIServiceError:
        raise
    except Exception as e:
        logger.error(f"Grievance draft error on {settings.GEMINI_MODEL}: {e}")
        raise AIServiceError(502, "Failed to generate grievance draft from AI. Please try again.")
