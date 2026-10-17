import io
import json
from typing import Dict, Any, Optional
from pypdf import PdfReader
from app.database import get_db

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extracts readable text from PDF byte content."""
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        extracted_text = []
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                extracted_text.append(f"--- Page {i+1} ---\n{page_text}")
        full_text = "\n\n".join(extracted_text).strip()
        if not full_text:
            raise ValueError("No readable text found in this PDF. It may contain scanned images or protected content.")
        return full_text
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")

def save_document_analysis(filename: str, file_type: str, raw_text: str, analysis: Dict[str, Any], session_id: str) -> int:
    """Saves verified analysis result to database scoped to worker session."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO document_analyses (
                session_id, filename, file_type, extracted_text, summary, 
                key_amounts, important_dates, conditions, checklist
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session_id,
            filename,
            file_type,
            raw_text[:50000],
            analysis.get("summary", ""),
            json.dumps(analysis.get("key_amounts", [])),
            json.dumps(analysis.get("important_dates", [])),
            json.dumps(analysis.get("conditions_and_clauses", [])),
            json.dumps(analysis.get("missing_info_checklist", []))
        ))
        conn.commit()
        return cursor.lastrowid

def get_document_analysis_by_id(doc_id: int, session_id: str) -> Optional[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM document_analyses WHERE id = ? AND session_id = ?", (doc_id, session_id))
        row = cursor.fetchone()
        if not row:
            return None
        res = dict(row)
        res["key_amounts"] = json.loads(res["key_amounts"]) if res["key_amounts"] else []
        res["important_dates"] = json.loads(res["important_dates"]) if res["important_dates"] else []
        res["conditions_and_clauses"] = json.loads(res["conditions"]) if res["conditions"] else []
        res["missing_info_checklist"] = json.loads(res["checklist"]) if res["checklist"] else []
        return res
