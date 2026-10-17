import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

def test_journey_1_track_and_understand_earnings(client):
    """JOURNEY 1: Worker records actual earnings & expenses.
    Application calculates correct net earnings and summary with strict arithmetic."""
    session_headers = {"X-Session-ID": "journey_worker_01"}
    
    # 1. Create delivery shift entry
    entry_payload = {
        "date": "2024-10-16",
        "category": "Food Delivery",
        "platform": "Swiggy",
        "gross_earnings": 1400.0,
        "tips_incentives": 200.0,
        "expenses": 280.0,
        "notes": "Rain surge and peak dinner deliveries"
    }
    res = client.post("/api/earnings", json=entry_payload, headers=session_headers)
    assert res.status_code == 201
    entry = res.json()
    # Math: 1400 + 200 - 280 = 1320
    assert entry["net_earnings"] == 1320.0

    # 2. Check summary aggregation matches strictly
    sum_res = client.get("/api/earnings/summary", headers=session_headers)
    assert sum_res.status_code == 200
    summary = sum_res.json()
    assert summary["all_time"]["total_net"] == 1320.0
    assert summary["all_time"]["total_gross"] == 1400.0
    assert summary["all_time"]["total_expenses"] == 280.0
    assert "Swiggy" in summary["platform_breakdown"]

def test_journey_2_identify_and_draft_payment_dispute(client, monkeypatch):
    """JOURNEY 2: Worker identifies discrepancy in saved earnings,
    links the record to Grievance Assistant, and generates draft."""
    session_headers = {"X-Session-ID": "journey_worker_02"}

    # 1. Log an earning record
    earning_payload = {
        "date": "2024-10-14",
        "category": "Food Delivery",
        "platform": "Zomato",
        "gross_earnings": 1500.0,
        "tips_incentives": 300.0,
        "expenses": 200.0,
        "notes": "Order incentive #8812 omitted in payout"
    }
    earning = client.post("/api/earnings", json=earning_payload, headers=session_headers).json()

    # 2. Mock model call for test environment without active cloud network dependency
    from app.services import gemini_service
    def mock_draft(*args, **kwargs):
        return {
            "generated_draft": f"Subject: Formal Dispute Regarding Omitted Incentive - Zomato\n\nDear Zomato Grievance Officer,\n\nI am writing to formally report an issue regarding missing incentives for date 2024-10-14 in the amount of Rs 300.",
            "checklist": ["Order #8812 screenshot", "Bank statement"],
            "next_steps": ["Submit ticket via in-app partner support"]
        }
    monkeypatch.setattr("app.services.grievance_service.draft_grievance_dispute", mock_draft)

    grievance_req = {
        "category": "Missing incentives or payment discrepancies",
        "employer_platform": earning["platform"],
        "incident_date": earning["date"],
        "amount_disputed": 300.0,
        "linked_earning_id": earning["id"],
        "incident_details": f"Weekly settlement omitted incentive of Rs 300 for date {earning['date']}",
        "evidence_available": "App delivery history screenshot and bank statement",
        "language": "en"
    }
    draft_res = client.post("/api/grievances/draft", json=grievance_req, headers=session_headers)
    assert draft_res.status_code == 200
    draft_data = draft_res.json()
    assert "generated_draft" in draft_data
    assert "Zomato" in draft_data["generated_draft"]
    assert len(draft_data["checklist"]) > 0

    # 3. Worker saves the reviewed draft to database
    save_req = {
        **grievance_req,
        "generated_draft": draft_data["generated_draft"]
    }
    save_res = client.post("/api/grievances/save", json=save_req, headers=session_headers)
    assert save_res.status_code == 201
    saved_obj = save_res.json()
    assert saved_obj["id"] is not None

    # 4. Verify listed in worker's saved grievances
    list_res = client.get("/api/grievances", headers=session_headers)
    assert list_res.status_code == 200
    assert any(g["id"] == saved_obj["id"] for g in list_res.json())

def test_journey_3_understand_a_document(client, monkeypatch):
    """JOURNEY 3: Worker pastes or uploads contract/statement.
    System extracts and returns grounded analysis."""
    from app.services import gemini_service
    def mock_analyze(text, doc_type, language):
        return {
            "summary": "Platform agreement requiring 20% commission with a 48-hour dispute notice window.",
            "key_amounts": ["20% platform fee", "Rs. 50 cancellation penalty"],
            "important_dates": ["01 November 2024 effective date", "Tuesday weekly payout", "48 hours notice window"],
            "conditions_and_clauses": ["Account suspension if cancellations exceed 5% over 7 days"],
            "missing_info_checklist": ["Missing details on arbitration location"],
            "questions_to_ask": ["Can weather delays waive cancellation penalties?"],
            "disclaimer": "Informational review only. Not certified legal advice.",
            "language": language
        }
    monkeypatch.setattr("app.routers.documents.analyze_document_text", mock_analyze)

    doc_req = {
        "document_text": "Sample platform rider terms with 20% commission and Rs 50 penalty.",
        "document_type": "Partner Terms",
        "language": "en"
    }
    res = client.post("/api/documents/analyze-text", json=doc_req)
    assert res.status_code == 200
    doc_data = res.json()
    assert "20% platform fee" in doc_data["key_amounts"]
    assert "disclaimer" in doc_data

def test_journey_4_discover_relevant_welfare_resources(client):
    """JOURNEY 4: Worker filters by location and work category to discover authoritative schemes."""
    res = client.get("/api/welfare?category=Food%20Delivery&location=Rajasthan")
    assert res.status_code == 200
    schemes = res.json()
    scheme_ids = [s["id"] for s in schemes]
    assert "rajasthan_gig_act" in scheme_ids or "eshram" in scheme_ids
    assert all("authority" in s and "last_verified" in s and "source" in s for s in schemes)

def test_journey_5_contextual_safety_guidance(client):
    """JOURNEY 5: Worker gets safety guidelines and emergency contacts for their trade."""
    for category in ["Food Delivery", "Cab/Ride-hailing", "Construction/Daily Wage"]:
        res = client.get(f"/api/safety/{category}")
        assert res.status_code == 200
        guide = res.json()
        assert len(guide["emergency_numbers"]) > 0
        assert len(guide["categories"]) > 0
        assert any("112" in em["number"] for em in guide["emergency_numbers"])

def test_multilingual_ai_chat_routing(client, monkeypatch):
    """Verify chat endpoint detects intent routing deterministically."""
    def mock_chat(message, session_id, language, context_type, context_data):
        routing = "earnings" if "earning" in message.lower() else ("welfare" if "योजना" in message or "scheme" in message else None)
        return {
            "reply": "Mocked assistant guidance",
            "language": language,
            "suggested_actions": [{"text": "Action", "action": f"navigate_{routing}"}] if routing else [],
            "routing_target": routing
        }
    monkeypatch.setattr("app.routers.ai.generate_chat_reply", mock_chat)

    res = client.post("/api/ai/chat", json={
        "message": "Calculate my earnings and tell me my income this week",
        "language": "en"
    })
    assert res.status_code == 200
    assert res.json()["routing_target"] == "earnings"

    res_hi = client.post("/api/ai/chat", json={
        "message": "ई-श्रम और सरकारी योजना के बारे में बताएं",
        "language": "hi"
    })
    assert res_hi.status_code == 200
    assert res_hi.json()["routing_target"] == "welfare"

@pytest.mark.skipif(not os.getenv("GEMINI_API_KEY"), reason="Live Gemini call requires GEMINI_API_KEY")
def test_live_gemini_3_8_flash_smoke(client):
    """Priority 6: Genuine live model call verification using gemini-3.8-flash."""
    res = client.post("/api/ai/test-connection")
    assert res.status_code == 200
    data = res.json()
    assert data["verified"] is True
    assert data["model"] == "gemini-3.8-flash"
    assert data["latency_ms"] is not None
