import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.core.redis_client import get_redis_client, close_redis_client
from app.api.v1.router import api_router

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
    description="Autonomous Corporate & Infrastructure Intelligence Terminal powered by FastAPI and Redis.",
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

# Mount PRISM // OS API v1 router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["System"])
@limiter.limit("60/minute")
async def health_check(request: Request):
    redis = await get_redis_client()
    redis_status = "connected" if redis else "fallback_active"
    return {
        "status": "online",
        "service": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "redis_status": redis_status,
        "timestamp": time.time(),
    }
