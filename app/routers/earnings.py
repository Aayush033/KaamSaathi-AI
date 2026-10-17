from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from app.models import EarningCreate, EarningUpdate, EarningResponse, EarningsSummaryResponse
from app.dependencies import get_or_create_session_id
from app.services.earnings_service import (
    create_earning_entry,
    get_all_earnings,
    get_earning_by_id,
    update_earning_entry,
    delete_earning_entry,
    get_earnings_summary
)

router = APIRouter(prefix="/api/earnings", tags=["Earnings"])

@router.post("", response_model=EarningResponse, status_code=201)
def create_earning(
    earning: EarningCreate,
    session_id: str = Depends(get_or_create_session_id)
):
    return create_earning_entry(earning, session_id=session_id)

@router.get("", response_model=List[EarningResponse])
def list_earnings(
    start_date: Optional[str] = Query(None, description="Filter from date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Filter to date (YYYY-MM-DD)"),
    category: Optional[str] = Query(None, description="Filter by category"),
    platform: Optional[str] = Query(None, description="Filter by platform"),
    session_id: str = Depends(get_or_create_session_id)
):
    return get_all_earnings(
        session_id=session_id,
        start_date=start_date,
        end_date=end_date,
        category=category,
        platform=platform
    )

@router.get("/summary", response_model=EarningsSummaryResponse)
def get_summary(session_id: str = Depends(get_or_create_session_id)):
    return get_earnings_summary(session_id=session_id)

@router.get("/{earning_id}", response_model=EarningResponse)
def get_earning(
    earning_id: int,
    session_id: str = Depends(get_or_create_session_id)
):
    entry = get_earning_by_id(earning_id, session_id=session_id)
    if not entry:
        raise HTTPException(status_code=404, detail=f"Earning entry #{earning_id} not found")
    return entry

@router.put("/{earning_id}", response_model=EarningResponse)
def update_earning(
    earning_id: int,
    updates: EarningUpdate,
    session_id: str = Depends(get_or_create_session_id)
):
    updated = update_earning_entry(earning_id, updates, session_id=session_id)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Earning entry #{earning_id} not found")
    return updated

@router.delete("/{earning_id}")
def delete_earning(
    earning_id: int,
    session_id: str = Depends(get_or_create_session_id)
):
    success = delete_earning_entry(earning_id, session_id=session_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Earning entry #{earning_id} not found")
    return {"status": "success", "message": f"Earning entry #{earning_id} deleted"}
