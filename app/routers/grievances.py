from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from app.models import GrievanceDraftRequest, GrievanceSaveRequest, GrievanceResponse
from app.services.grievance_service import (
    generate_and_prepare_draft,
    save_grievance,
    get_saved_grievances,
    get_grievance_by_id
)
from app.services.gemini_service import AIServiceError
from app.services.rate_limiter import check_ai_rate_limit
from app.dependencies import get_or_create_session_id

router = APIRouter(prefix="/api/grievances", tags=["Grievance & Disputes"])

@router.post("/draft", response_model=GrievanceResponse)
def create_draft(
    req: GrievanceDraftRequest,
    session_id: str = Depends(get_or_create_session_id),
    _: None = Depends(check_ai_rate_limit)
):
    try:
        return generate_and_prepare_draft(req, session_id=session_id)
    except AIServiceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=502, detail="Failed to generate grievance draft. Please try again.")

@router.post("/save", response_model=GrievanceResponse, status_code=201)
def save_draft(
    req: GrievanceSaveRequest,
    session_id: str = Depends(get_or_create_session_id)
):
    return save_grievance(req, session_id=session_id)

@router.get("", response_model=List[Dict[str, Any]])
def list_grievances(session_id: str = Depends(get_or_create_session_id)):
    return get_saved_grievances(session_id=session_id)

@router.get("/{grievance_id}")
def get_grievance(
    grievance_id: int,
    session_id: str = Depends(get_or_create_session_id)
):
    item = get_grievance_by_id(grievance_id, session_id=session_id)
    if not item:
        raise HTTPException(status_code=404, detail="Grievance record not found or access denied.")
    return item
