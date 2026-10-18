import redis.asyncio as aioredis
from typing import Optional
from app.core.config import settings

redis_pool: Optional[aioredis.Redis] = None


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
            return None
    return redis_pool


async def close_redis_client():
    global redis_pool
    if redis_pool is not None:
        await redis_pool.close()
        redis_pool = None
