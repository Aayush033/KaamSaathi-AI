from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from typing import Optional
from app.models import DocumentAnalyzeTextRequest, DocumentAnalyzeResponse
from app.services.gemini_service import analyze_document_text, AIServiceError
from app.services.document_service import extract_text_from_pdf, save_document_analysis, get_document_analysis_by_id
from app.services.rate_limiter import check_ai_rate_limit
from app.dependencies import get_or_create_session_id
from app.config import settings

router = APIRouter(prefix="/api/documents", tags=["Document Assistant"])

@router.post("/analyze-text", response_model=DocumentAnalyzeResponse)
def analyze_text_endpoint(
    req: DocumentAnalyzeTextRequest,
    session_id: str = Depends(get_or_create_session_id),
    _: None = Depends(check_ai_rate_limit)
):
    text = req.document_text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Document text cannot be empty.")
    if len(text) > 100_000:
        raise HTTPException(status_code=413, detail="Document text exceeds maximum length of 100,000 characters.")
        
    try:
        analysis = analyze_document_text(
            text=text,
            doc_type=req.document_type or "General Document",
            language=req.language or "en"
        )
    except AIServiceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=502, detail="AI document analysis failed. Please try again.")
    
    # Save to history ONLY after genuine AI success
    save_document_analysis(
        filename="Pasted_Document_Text",
        file_type="text/plain",
        raw_text=text,
        analysis=analysis,
        session_id=session_id
    )
    
    return DocumentAnalyzeResponse(
        summary=analysis.get("summary", ""),
        key_amounts=analysis.get("key_amounts", []),
        important_dates=analysis.get("important_dates", []),
        conditions_and_clauses=analysis.get("conditions_and_clauses", []),
        missing_info_checklist=analysis.get("missing_info_checklist", []),
        questions_to_ask=analysis.get("questions_to_ask", []),
        disclaimer=analysis.get("disclaimer", "Informational only."),
        language=req.language or "en"
    )

@router.post("/upload")
async def upload_document_endpoint(
    file: UploadFile = File(...),
    document_type: str = Form("General Document"),
    language: str = Form("en"),
    session_id: str = Depends(get_or_create_session_id),
    _: None = Depends(check_ai_rate_limit)
):
    # Enforce maximum upload size limit (5 MB)
    contents = await file.read()
    if len(contents) > settings.MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"Uploaded file exceeds maximum limit of {settings.MAX_UPLOAD_BYTES // (1024 * 1024)} MB."
        )

    filename = file.filename or "uploaded_doc"
    lower_name = filename.lower()
    
    if lower_name.endswith(".pdf"):
        try:
            raw_text = extract_text_from_pdf(contents)
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"PDF extraction error: {str(e)}")
    elif lower_name.endswith((".txt", ".csv")):
        try:
            raw_text = contents.decode("utf-8")
        except UnicodeDecodeError:
            raw_text = contents.decode("latin-1")
    else:
        raise HTTPException(
            status_code=400, 
            detail="Unsupported file format. Please upload a PDF or plain text (.txt, .csv) file, or paste text directly."
        )

    if not raw_text.strip():
        raise HTTPException(status_code=422, detail="No readable text could be extracted from the uploaded document.")

    try:
        analysis = analyze_document_text(text=raw_text, doc_type=document_type, language=language)
    except AIServiceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=502, detail="Document analysis failed. Please try again.")
    
    # Save to history ONLY after verified AI success
    doc_id = save_document_analysis(
        filename=filename,
        file_type=file.content_type or "application/octet-stream",
        raw_text=raw_text,
        analysis=analysis,
        session_id=session_id
    )
    
    return {
        "id": doc_id,
        "filename": filename,
        "analysis": analysis,
        "raw_text_preview": raw_text[:300] + ("..." if len(raw_text) > 300 else "")
    }

@router.get("/{doc_id}")
def get_document_details(
    doc_id: int,
    session_id: str = Depends(get_or_create_session_id)
):
    doc = get_document_analysis_by_id(doc_id, session_id=session_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document record not found or access denied.")
    return doc
