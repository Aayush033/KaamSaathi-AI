import time
from collections import defaultdict
from threading import Lock
from typing import Dict, List
from fastapi import Request, HTTPException, Depends
from app.config import settings
from app.dependencies import get_or_create_session_id

# Note on Architecture:
# This in-memory rate limiter provides per-container rate limiting for public AI endpoints
# without introducing complicated external infrastructure (e.g. Redis/Memcached).
# In multi-instance Google Cloud Run environments, this controls burst requests per container.
# For global distributed rate limiting across multiple instances, GCP Cloud Armor or an API Gateway is recommended.

class InMemoryRateLimiter:
    def __init__(self, requests_per_minute: int = 20):
        self.requests_per_minute = requests_per_minute
        self.window_seconds = 60
        self._history: Dict[str, List[float]] = defaultdict(list)
        self._lock = Lock()

    def is_allowed(self, client_key: str) -> bool:
        now = time.time()
        window_start = now - self.window_seconds
        with self._lock:
            # Filter out timestamps outside window
            timestamps = [t for t in self._history[client_key] if t > window_start]
            if len(timestamps) >= self.requests_per_minute:
                self._history[client_key] = timestamps
                return False
            timestamps.append(now)
            self._history[client_key] = timestamps
            return True

    def reset_all(self):
        """Used in test fixtures if needed."""
        with self._lock:
            self._history.clear()

ai_rate_limiter = InMemoryRateLimiter(requests_per_minute=settings.AI_RATE_LIMIT_PER_MINUTE)

def check_ai_rate_limit(
    request: Request,
    session_id: str = Depends(get_or_create_session_id)
) -> None:
    """FastAPI dependency to protect public AI endpoints from abuse."""
    client_ip = request.client.host if request.client else "unknown"
    rate_key = f"{session_id}:{client_ip}"
    if not ai_rate_limiter.is_allowed(rate_key):
        raise HTTPException(
            status_code=429,
            detail="Too many AI requests. Please wait a moment before sending another request.",
            headers={"Retry-After": "60"}
        )
