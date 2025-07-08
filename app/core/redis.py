import redis
from app.core.settings import settings

redis_pool = redis.ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    db=0,
    decode_responses=True,
    max_connections=10
)

def get_redis():
    """Зависимость для FastAPI или других компонентов."""
    return redis.Redis(connection_pool=redis_pool)