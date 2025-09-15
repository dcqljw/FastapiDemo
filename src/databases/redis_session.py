from typing import Any, AsyncGenerator

import redis.asyncio as redis
from redis.asyncio import Redis

from src.core.settings import settings

redis_pool = redis.ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    decode_responses=True,
    encoding='utf-8',
    max_connections=10
)


async def get_redis() -> AsyncGenerator[Redis, Any]:
    redis_client = redis.Redis(connection_pool=redis_pool)
    try:
        yield redis_client
    finally:
        await redis_client.aclose()
