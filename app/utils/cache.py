import logging
import json
from functools import wraps
from typing import Any, Callable, Coroutine
from redis.asyncio import Redis
from app.core.redis import get_redis
from datetime import datetime

logger = logging.getLogger(__name__)

def json_serializer(obj):
    """Кастомный сериализатор для JSON"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def cache_result(expiration_time: int = 300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"cache:{func.__name__}:{args}:{kwargs}"
            redis_client = await get_redis()
            # Проверка кеша
            cached = await redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # Выполнение функции
            result = await func(*args, **kwargs)
            
            # Сериализация с обработкой datetime
            await redis_client.set(
                cache_key,
                json.dumps(result, default=json_serializer),
                ex=expiration_time
            )
            return result
        return wrapper
    return decorator
