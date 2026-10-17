from fastapi import APIRouter, Query, HTTPException
from typing import List, Dict, Any, Optional
from app.services.welfare_service import search_welfare_schemes, get_scheme_by_id

router = APIRouter(prefix="/api/welfare", tags=["Welfare & Rights"])

@router.get("", response_model=List[Dict[str, Any]])
def get_schemes(
    category: Optional[str] = Query(None, description="Worker category filter"),
    location: Optional[str] = Query(None, description="State or location filter"),
    query: Optional[str] = Query(None, description="Search term")
):
    return search_welfare_schemes(category=category, location=location, query=query)

@router.get("/{scheme_id}", response_model=Dict[str, Any])
def get_scheme(scheme_id: str):
    scheme = get_scheme_by_id(scheme_id)
    if not scheme:
        raise HTTPException(status_code=404, detail="Welfare scheme not found")
    return scheme
