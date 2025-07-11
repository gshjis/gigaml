import redis
from typing import Any
from app.core.settings import settings

redis_pool = redis.ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    db=0,
    decode_responses=True,
    max_connections=10,
)

def get_redis() -> Any:
    """
    Get a Redis connection.

    Returns:
        redis.Redis: A Redis connection.
    """
    try:
        return redis.Redis(connection_pool=redis_pool)
    except redis.ConnectionError as e:
        print(f"Error connecting to Redis: {e}")
        return None
