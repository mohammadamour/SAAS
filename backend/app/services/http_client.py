import re
import httpx
from typing import Optional
from app.core.config import settings

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 PRISM-OS/1.0"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


def sanitize_domain(raw_input: str) -> str:
    """
    Cleans any URL or domain input to a bare, lowercased domain.
    e.g., 'https://www.spotify.com/us/premium?ref=1' -> 'spotify.com'
    """
    cleaned = raw_input.strip().lower()
    # Remove protocol
    cleaned = re.sub(r"^https?://", "", cleaned)
    # Remove www.
    cleaned = re.sub(r"^www\.", "", cleaned)
    # Strip any path, query, or hash
    cleaned = cleaned.split("/")[0].split("?")[0].split("#")[0]
    return cleaned


def get_async_client() -> httpx.AsyncClient:
    """
    Returns an async HTTP client configured with reasonable timeouts and browser headers.
    """
    return httpx.AsyncClient(
        timeout=settings.REQUEST_TIMEOUT_SECONDS,
        headers=HEADERS,
        follow_redirects=True,
    )
