import json
import time
from typing import Dict, Optional, Tuple
import redis.asyncio as aioredis
from app.core.config import settings

redis_pool: Optional[aioredis.Redis] = None

# Resilient in-memory fallback buffer (stores {key: (payload, expire_timestamp)})
_local_memory_cache: Dict[str, Tuple[dict, float]] = {}


async def get_redis_client() -> Optional[aioredis.Redis]:
    global redis_pool
    if redis_pool is None:
        try:
            redis_pool = aioredis.from_url(
                settings.redis_url,
                encoding="utf-8",
                decode_responses=True,
                socket_connect_timeout=2,
            )
            # Test ping
            await redis_pool.ping()
        except Exception as e:
            print(f"[Redis Warning] Could not connect to Redis at {settings.redis_url}: {e}")
            redis_pool = None
            return None
    return redis_pool


async def close_redis_client():
    global redis_pool
    if redis_pool is not None:
        await redis_pool.close()
        redis_pool = None


async def get_cached_dossier(domain: str) -> Optional[dict]:
    """
    Retrieves cached dossier by domain. Checks Redis first, falls back to memory buffer.
    """
    cache_key = f"prism:dossier:{domain.lower().strip()}"
    client = await get_redis_client()

    # 1. Try Redis
    if client:
        try:
            raw_data = await client.get(cache_key)
            if raw_data:
                return json.loads(raw_data)
        except Exception as exc:
            print(f"[Redis Cache Read Error] {exc}")

    # 2. In-Memory Fallback
    if cache_key in _local_memory_cache:
        payload, expires_at = _local_memory_cache[cache_key]
        if time.time() < expires_at:
            return payload
        else:
            del _local_memory_cache[cache_key]

    return None


async def set_cached_dossier(domain: str, payload: dict, ttl: int = 86400) -> bool:
    """
    Caches company dossier with a default 24-hour TTL (86,400s).
    """
    cache_key = f"prism:dossier:{domain.lower().strip()}"
    client = await get_redis_client()
    json_str = json.dumps(payload)

    # 1. Write to Redis if available
    saved_to_redis = False
    if client:
        try:
            await client.setex(cache_key, ttl, json_str)
            saved_to_redis = True
        except Exception as exc:
            print(f"[Redis Cache Write Error] {exc}")

    # 2. Always maintain in-memory fallback buffer
    _local_memory_cache[cache_key] = (payload, time.time() + ttl)
    return True


async def get_cache_stats() -> dict:
    """
    Returns live metrics on Redis connection status and cache utilization.
    """
    client = await get_redis_client()
    if client:
        try:
            info = await client.info("memory")
            keys = await client.keys("prism:dossier:*")
            return {
                "engine": "Redis In-Memory Cluster",
                "status": "connected",
                "cached_dossiers_count": len(keys),
                "used_memory_human": info.get("used_memory_human", "N/A"),
                "fallback_active": False,
            }
        except Exception:
            pass

    return {
        "engine": "Local In-Memory Buffer",
        "status": "fallback_active",
        "cached_dossiers_count": len(_local_memory_cache),
        "used_memory_human": "Embedded RAM",
        "fallback_active": True,
    }
