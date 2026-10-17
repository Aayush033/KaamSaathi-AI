import os
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.config import settings
from app.database import init_db, check_db_health
from app.routers import earnings, ai, documents, grievances, welfare, safety

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="KaamSaathi AI - Generative AI Assistant for Gig and Informal Workers in India",
    lifespan=lifespan
)

# Secure CORS: Default to same-origin / local development origins rather than wildcard '*'
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000")
allowed_origins = [orig.strip() for orig in allowed_origins_env.split(",") if orig.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(earnings.router)
app.include_router(ai.router)
app.include_router(documents.router)
app.include_router(grievances.router)
app.include_router(welfare.router)
app.include_router(safety.router)

# Mount Static Files
STATIC_DIR = Path(__file__).resolve().parent / "static"
STATIC_DIR.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

from app.services.gemini_service import get_verification_status

@app.get("/health")
def health_check():
    db_ok = check_db_health()
    key_configured = bool(settings.get_api_key())
    ver_status = get_verification_status()
    
    return {
        "status": "healthy" if db_ok else "unhealthy",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "database_connected": db_ok,
        "api_key_configured": key_configured,
        "model_verified": ver_status.get("verified", False),
        "last_verified_at": ver_status.get("last_tested_at"),
        "model": settings.GEMINI_MODEL
    }

@app.get("/")
def serve_index():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "KaamSaathi AI API is running."}
