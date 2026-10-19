import time
from fastapi import APIRouter, Request, HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.schemas.dossier import PrismDossierResponse
from app.services.http_client import sanitize_domain
from app.services.intelligence_service import aggregate_company_dossier, CURATED_BRANDS
from app.core.redis_client import get_cached_dossier, set_cached_dossier, get_cache_stats

limiter = Limiter(key_func=get_remote_address)
api_router = APIRouter()


@api_router.get("/intel/{domain:path}", response_model=PrismDossierResponse, tags=["PRISM Intelligence"])
@limiter.limit("30/minute")
async def get_company_intelligence(request: Request, domain: str):
    """
    Ingests 4 concurrent streams for any domain:
    1. Brand & Identity (Palette, vector logo, bio)
    2. Global Edge Cloud & Network Telemetry (AWS/Cloudflare, TTFB, SSL validity)
    3. Web Performance & Core Vitals (Lighthouse score rings)
    4. AI Strategic Intelligence (Unfiltered 1-liner, moat, vulnerability, rivals)
    
    Sub-millisecond Redis caching with 24-hour TTL.
    """
    clean_domain = sanitize_domain(domain)
    if not clean_domain or "." not in clean_domain:
        raise HTTPException(
            status_code=400,
            detail="Invalid domain format. Please provide a valid domain (e.g. spotify.com, stripe.com).",
        )

    # 1. Check In-Memory Buffer / Redis Cache
    cache_start = time.perf_counter()
    cached_data = await get_cached_dossier(clean_domain)
    if cached_data:
        retrieval_ms = round((time.perf_counter() - cache_start) * 1000, 2)
        cached_data["cached"] = True
        cached_data["processing_time_ms"] = retrieval_ms
        return PrismDossierResponse(**cached_data)

    # 2. Cache MISS: Concurrently aggregate all 4 data streams
    try:
        dossier = await aggregate_company_dossier(clean_domain)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to gather intelligence streams for '{clean_domain}': {str(exc)}",
        )

    # 3. Store in Redis with 24h TTL
    await set_cached_dossier(clean_domain, dossier.model_dump(), ttl=86400)

    return dossier


@api_router.get("/cache/stats", tags=["System Telemetry"])
@limiter.limit("60/minute")
async def cache_telemetry(request: Request):
    """
    Returns live in-memory Redis cluster statistics and cached dossier counters.
    """
    stats = await get_cache_stats()
    return stats


@api_router.get("/presets", tags=["System Telemetry"])
@limiter.limit("60/minute")
async def get_curated_presets(request: Request):
    """
    Returns pre-curated high-performance corporate presets for instant 1-click exploration.
    """
    presets = []
    for domain, item in CURATED_BRANDS.items():
        presets.append({
            "domain": domain,
            "name": item["name"],
            "primary_color": item["primary_color"],
            "secondary_color": item["secondary_color"],
        })
    return {"presets": presets}
