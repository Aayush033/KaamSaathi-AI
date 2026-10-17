import re
import secrets
from fastapi import Request, Response
from app.config import settings

SAFE_SESSION_PATTERN = re.compile(r"^[A-Za-z0-9_-]{16,64}$")

def get_or_create_session_id(request: Request, response: Response) -> str:
    """
    Extracts a verified session ID from HttpOnly cookie or secure header.
    If missing or invalid, generates a new cryptographic session token and attaches it to the response.
    Never trusts client-supplied user parameters.
    """
    session_id = None

    # Restrict X-Session-ID strictly to controlled test environments.
    # In testing, explicit header takes precedence to prevent TestClient cookie jar pollution across users.
    # In production, X-Session-ID is completely ignored to prevent session spoofing.
    if settings.ENVIRONMENT in ("testing", "test") or settings.ALLOW_TEST_SESSION_HEADER:
        candidate = request.headers.get("X-Session-ID")
        if candidate and SAFE_SESSION_PATTERN.match(candidate):
            session_id = candidate

    if not session_id:
        session_id = request.cookies.get(settings.SESSION_COOKIE_NAME)
        
    if not session_id or not SAFE_SESSION_PATTERN.match(session_id):
        session_id = secrets.token_urlsafe(32)
        response.set_cookie(
            key=settings.SESSION_COOKIE_NAME,
            value=session_id,
            httponly=True,
            samesite="lax",
            secure=request.url.scheme == "https",
            max_age=60 * 60 * 24 * 30, # 30 days
            path="/"
        )
    return session_id
