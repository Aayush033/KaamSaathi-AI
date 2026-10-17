from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from app.config import settings
from app.models import ChatRequest, ChatResponse, SystemStatusResponse, TestConnectionResponse
from app.services.gemini_service import (
    generate_chat_reply,
    explain_earnings,
    is_api_configured,
    test_ai_connection,
    get_verification_status,
    AIServiceError
)
from app.services.earnings_service import get_earnings_summary, get_all_earnings
from app.services.rate_limiter import check_ai_rate_limit
from app.dependencies import get_or_create_session_id
from app.database import check_db_health

router = APIRouter(prefix="/api/ai", tags=["AI Assistant"])

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(
    req: ChatRequest,
    session_id: str = Depends(get_or_create_session_id),
    _: None = Depends(check_ai_rate_limit)
):
    try:
        result = generate_chat_reply(
            message=req.message,
            session_id=session_id,
            language=req.language or "en",
            context_type=req.context_type,
            context_data=req.context_data
        )
        return ChatResponse(
            reply=result["reply"],
            suggested_actions=result.get("suggested_actions", []),
            routing_target=result.get("routing_target"),
            language=result["language"]
        )
    except AIServiceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=502, detail="AI chat service is temporarily unavailable. Please try again.")

@router.post("/explain-earnings")
def explain_earnings_endpoint(
    payload: Dict[str, Any],
    session_id: str = Depends(get_or_create_session_id),
    _: None = Depends(check_ai_rate_limit)
):
    language = payload.get("language", "en")
    summary = get_earnings_summary(session_id=session_id).model_dump()
    recent = [e.model_dump() for e in get_all_earnings(session_id=session_id)[:5]]
    
    try:
        explanation = explain_earnings(summary, recent, language)
        return {"explanation": explanation, "language": language}
    except AIServiceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=502, detail="Failed to generate earnings explanation. Please try again.")

@router.get("/status", response_model=SystemStatusResponse)
def get_system_status():
    """Reports honest system status without invoking Gemini on every request."""
    db_ok = check_db_health()
    configured = is_api_configured()
    ver_status = get_verification_status()
    verified = ver_status.get("verified", False)
    last_verified = ver_status.get("last_tested_at")

    if not db_ok:
        status_label = "degraded"
    elif verified:
        status_label = "verified"
    elif configured:
        status_label = "configured_unverified"
    else:
        status_label = "not_configured"

    return SystemStatusResponse(
        status=status_label,
        api_key_configured=configured,
        model_verified=verified,
        last_verified_at=last_verified,
        model_name=settings.GEMINI_MODEL,
        database_connected=db_ok,
        version=settings.VERSION
    )

@router.post("/test-connection", response_model=TestConnectionResponse)
def test_connection_endpoint():
    """Performs an explicit live model call to test Gemini availability and updates verification status."""
    result = test_ai_connection()
    return TestConnectionResponse(**result)
