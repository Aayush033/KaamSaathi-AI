from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

# --- Earnings Models ---
class EarningBase(BaseModel):
    date: str = Field(..., description="Date of work in YYYY-MM-DD format")
    category: str = Field(..., description="Worker category e.g. Food Delivery, Cab Driver, Daily Wage")
    platform: str = Field(..., description="Platform/Employer name e.g. Zomato, Uber, Swiggy, Offline")
    gross_earnings: float = Field(..., ge=0, description="Gross base earnings")
    tips_incentives: float = Field(default=0.0, ge=0, description="Tips, peak pay, bonuses")
    expenses: float = Field(default=0.0, ge=0, description="Fuel, vehicle maintenance, tolls, commission")
    notes: Optional[str] = Field(default=None, description="Additional notes or trip counts")

class EarningCreate(EarningBase):
    pass

class EarningUpdate(BaseModel):
    date: Optional[str] = None
    category: Optional[str] = None
    platform: Optional[str] = None
    gross_earnings: Optional[float] = Field(default=None, ge=0)
    tips_incentives: Optional[float] = Field(default=None, ge=0)
    expenses: Optional[float] = Field(default=None, ge=0)
    notes: Optional[str] = None

class EarningResponse(EarningBase):
    id: int
    net_earnings: float
    created_at: str

class PeriodSummary(BaseModel):
    period: str
    total_gross: float
    total_tips: float
    total_expenses: float
    total_net: float
    entry_count: int

class EarningsSummaryResponse(BaseModel):
    today: PeriodSummary
    this_week: PeriodSummary
    this_month: PeriodSummary
    all_time: PeriodSummary
    category_breakdown: Dict[str, float]
    platform_breakdown: Dict[str, float]

# --- AI Chat Models ---
class ChatMessage(BaseModel):
    role: str
    content: str
    language: Optional[str] = "en"

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000, description="User message (max 4,000 characters)")
    session_id: Optional[str] = "default"
    language: Optional[str] = "en"
    context_type: Optional[str] = None # 'earnings', 'safety', 'scheme', 'document', 'grievance'
    context_data: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    reply: str
    suggested_actions: Optional[List[Dict[str, str]]] = []
    routing_target: Optional[str] = None
    language: str

# --- Grievance Models ---
class GrievanceDraftRequest(BaseModel):
    category: str
    employer_platform: str
    incident_date: str
    amount_disputed: Optional[float] = None
    linked_earning_id: Optional[int] = None
    incident_details: str = Field(..., min_length=5, max_length=5000, description="Grievance description (max 5,000 characters)")
    evidence_available: Optional[str] = None
    language: Optional[str] = "en"

class GrievanceSaveRequest(GrievanceDraftRequest):
    generated_draft: str

class GrievanceResponse(BaseModel):
    id: Optional[int] = None
    category: str
    employer_platform: str
    incident_date: str
    amount_disputed: Optional[float] = None
    linked_earning_id: Optional[int] = None
    incident_details: str
    evidence_available: Optional[str] = None
    generated_draft: str
    checklist: List[str] = []
    next_steps: List[str] = []
    language: str

# --- Document Analysis Models ---
class DocumentAnalyzeTextRequest(BaseModel):
    document_text: str = Field(..., min_length=1, max_length=100000)
    document_type: Optional[str] = "General Document"
    language: Optional[str] = "en"

class DocumentAnalyzeResponse(BaseModel):
    summary: str
    key_amounts: List[str]
    important_dates: List[str]
    conditions_and_clauses: List[str]
    missing_info_checklist: List[str]
    questions_to_ask: List[str]
    disclaimer: str
    language: str

# --- System / Status Models ---
class TestConnectionResponse(BaseModel):
    verified: bool
    model: str
    message: Optional[str] = None
    latency_ms: Optional[int] = None
    error: Optional[str] = None

class SystemStatusResponse(BaseModel):
    status: str
    api_key_configured: bool
    model_verified: bool
    last_verified_at: Optional[str] = None
    model_name: str
    database_connected: bool
    version: str
