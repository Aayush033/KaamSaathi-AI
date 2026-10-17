import sqlite3
from typing import List, Dict, Any, Optional
from app.database import get_db
from app.models import GrievanceDraftRequest, GrievanceSaveRequest, GrievanceResponse
from app.services.earnings_service import get_earning_by_id
from app.services.gemini_service import draft_grievance_dispute

def generate_and_prepare_draft(req: GrievanceDraftRequest, session_id: str) -> GrievanceResponse:
    linked_earning_dict = None
    if req.linked_earning_id:
        earning_obj = get_earning_by_id(req.linked_earning_id, session_id=session_id)
        if earning_obj:
            linked_earning_dict = earning_obj.model_dump()
            
    ai_result = draft_grievance_dispute(
        category=req.category,
        employer_platform=req.employer_platform,
        incident_date=req.incident_date,
        amount_disputed=req.amount_disputed,
        incident_details=req.incident_details,
        evidence_available=req.evidence_available,
        language=req.language or "en",
        linked_earning=linked_earning_dict
    )
    
    return GrievanceResponse(
        category=req.category,
        employer_platform=req.employer_platform,
        incident_date=req.incident_date,
        amount_disputed=req.amount_disputed,
        linked_earning_id=req.linked_earning_id if linked_earning_dict else None,
        incident_details=req.incident_details,
        evidence_available=req.evidence_available,
        generated_draft=ai_result.get("generated_draft", ""),
        checklist=ai_result.get("checklist", []),
        next_steps=ai_result.get("next_steps", []),
        language=req.language or "en"
    )

def save_grievance(req: GrievanceSaveRequest, session_id: str) -> GrievanceResponse:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO grievances (
                session_id, category, employer_platform, incident_date, amount_disputed,
                linked_earning_id, incident_details, evidence_available,
                generated_draft, language, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'draft')
        """, (
            session_id,
            req.category,
            req.employer_platform,
            req.incident_date,
            req.amount_disputed,
            req.linked_earning_id,
            req.incident_details,
            req.evidence_available,
            req.generated_draft,
            req.language or "en"
        ))
        conn.commit()
        new_id = cursor.lastrowid
        cursor.execute("SELECT * FROM grievances WHERE id = ? AND session_id = ?", (new_id, session_id))
        row = cursor.fetchone()
        r_dict = dict(row)
        return GrievanceResponse(
            id=r_dict["id"],
            category=r_dict["category"],
            employer_platform=r_dict["employer_platform"],
            incident_date=r_dict["incident_date"],
            amount_disputed=r_dict["amount_disputed"],
            linked_earning_id=r_dict["linked_earning_id"],
            incident_details=r_dict["incident_details"],
            evidence_available=r_dict["evidence_available"],
            generated_draft=r_dict["generated_draft"],
            checklist=["Platform application screenshot", "Bank transaction receipt", "Platform communication / ticket reference"],
            next_steps=["Submit draft via official platform support portal", "Preserve copy and ticket reference number"],
            language=r_dict["language"]
        )

def get_saved_grievances(session_id: str) -> List[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM grievances WHERE session_id = ? ORDER BY id DESC", (session_id,))
        rows = cursor.fetchall()
        return [dict(r) for r in rows]

def get_grievance_by_id(gid: int, session_id: str) -> Optional[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM grievances WHERE id = ? AND session_id = ?", (gid, session_id))
        row = cursor.fetchone()
        return dict(row) if row else None
