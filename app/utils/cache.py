from functools import wraps

from redis import Redis
from app.core.redis import redis_client

def cache_result(expiration_time: int = 300):
    """Redis caching decorator"""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"cache:{func.__name__}:{args}:{kwargs}"
            cached_result = redis_client.get(cache_key)

            if cached_result:
                return cached_result

            result = await func(*args, **kwargs)
            redis_client.set(cache_key, result, ex=expiration_time)

            return result

        return wrapper

    return decorator
