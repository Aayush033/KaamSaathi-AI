from fastapi import APIRouter
from typing import Dict, Any, List
from app.services.safety_service import get_safety_guide, get_all_safety_categories

router = APIRouter(prefix="/api/safety", tags=["Safety Guidance"])

@router.get("/categories", response_model=List[str])
def list_categories():
    return get_all_safety_categories()

@router.get("/{category:path}")
def get_guide_for_category(category: str):
    return get_safety_guide(category)
