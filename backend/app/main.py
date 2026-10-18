import time
import httpx
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.core.redis_client import get_redis_client, close_redis_client

limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize Redis pool
    await get_redis_client()
    yield
    # Shutdown: Close Redis pool
    await close_redis_client()


app = FastAPI(
    title=settings.APP_NAME,
    description="High-performance telemetry and SaaS API engine powered by FastAPI and Redis.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Attach rate limit error handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS setup for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class InspectRequest(BaseModel):
    url: str


class InspectResponse(BaseModel):
    target_url: str
    status_code: int
    response_time_ms: float
    is_https: bool
    server_header: str
    cached: bool
    ttl_seconds: int


@app.get("/health", tags=["System"])
@limiter.limit("60/minute")
async def health_check(request: Request):
    redis = await get_redis_client()
    redis_status = "connected" if redis else "unavailable"
    return {
        "status": "online",
        "service": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "redis_status": redis_status,
        "timestamp": time.time(),
    }


@app.post("/api/v1/inspect-endpoint", response_model=InspectResponse, tags=["Telemetry Engine"])
@limiter.limit("15/minute")
async def inspect_endpoint(request: Request, payload: InspectRequest):
    """
    Probes any URL in real-time, measures response latency, and caches telemetry in Redis.
    Demonstrates:
    - Distributed caching with TTL
    - Rate-limiting via SlowAPI
    - Async non-blocking network I/O
    """
    target = payload.url.strip()
    if not target.startswith("http://") and not target.startswith("https://"):
        target = "https://" + target

    cache_key = f"telemetry:{target}"
    redis = await get_redis_client()

    # 1. Check Redis Cache
    if redis:
        try:
            cached_data = await redis.hgetall(cache_key)
            if cached_data:
                ttl = await redis.ttl(cache_key)
                return InspectResponse(
                    target_url=cached_data["target_url"],
                    status_code=int(cached_data["status_code"]),
                    response_time_ms=float(cached_data["response_time_ms"]),
                    is_https=cached_data["is_https"] == "True",
                    server_header=cached_data.get("server_header", "unknown"),
                    cached=True,
                    ttl_seconds=ttl,
                )
        except Exception as e:
            print(f"[Cache Read Error] {e}")

    # 2. Live Probe via Async HTTPX
    start_time = time.perf_counter()
    try:
        async with httpx.AsyncClient(timeout=8.0, follow_redirects=True) as client:
            resp = await client.get(target)
            latency = round((time.perf_counter() - start_time) * 1000, 2)
            server = resp.headers.get("server", "hidden / cloudflare")
            is_https = target.startswith("https://")
            status_code = resp.status_code
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to reach destination endpoint: {str(exc)}",
        )

    # 3. Cache into Redis for 60 seconds
    if redis:
        try:
            telemetry_payload = {
                "target_url": target,
                "status_code": str(status_code),
                "response_time_ms": str(latency),
                "is_https": str(is_https),
                "server_header": server,
            }
            await redis.hset(cache_key, mapping=telemetry_payload)
            await redis.expire(cache_key, 60)
        except Exception as e:
            print(f"[Cache Write Error] {e}")

    return InspectResponse(
        target_url=target,
        status_code=status_code,
        response_time_ms=latency,
        is_https=is_https,
        server_header=server,
        cached=False,
        ttl_seconds=60,
    )
