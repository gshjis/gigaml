import logging
from typing import Optional

import redis.asyncio as aioredis

from app.core.settings import settings

logger = logging.getLogger(__name__)


async def get_redis() -> Optional[aioredis.Redis]:
    """
    Get an async Redis connection.

    Returns:
        aioredis.Redis: An async Redis connection.
    """
    try:
        redis_client = aioredis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=0,
            decode_responses=True,
            max_connections=10,
        )
        await redis_client.ping()
        return redis_client
    except aioredis.ConnectionError as e:
        logger.error(f"Error connecting to Redis: {e}")
        return None
