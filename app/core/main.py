from fastapi import FastAPI
from app.core.logging_config import logger
from app.core.settings import settings
from app.handlers import routers
from app.core.database import engine
from app.core.redis import get_redis

app = FastAPI()

logger.info("Application started")

# Initialize Redis connection
@app.on_event("startup")
async def startup():
    logger.info("Initializing connections...")
    app.state.redis = await get_redis()
    if app.state.redis is None:
        logger.error("Failed to initialize Redis connection")
        raise Exception("Failed to initialize Redis connection")

# Close connections on shutdown
@app.on_event("shutdown")
async def shutdown():
    logger.info("Closing connections...")
    if app.state.redis:
        await app.state.redis.close()
        logger.info("Redis connection closed")
    await engine.dispose()

for router in routers:
    app.include_router(router)
