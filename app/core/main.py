from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.logging_config import logger
from app.handlers import routers
from app.core.database import get_db_session, engine
from app.core.redis import get_redis
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Initializing application...")
    
    # Redis connection
    logger.info("Connecting to Redis...")
    app.state.redis = await get_redis()
    if not app.state.redis:
        logger.error("Redis connection failed!")
        raise RuntimeError("Redis connection failed")
    logger.info("Redis connected successfully")
    
    # Verify DB connection
    logger.info("Verifying database connection...")
    await anext(get_db_session())
    logger.info("Database connection verified")
    
    yield  # App runs here
    
    # Shutdown
    logger.info("Shutting down application...")
    
    if hasattr(app.state, "redis") and app.state.redis:
        logger.info("Closing Redis connection...")
        await app.state.redis.close()
    
    logger.info("Disposing database engine...")
    await engine.dispose()
    logger.info("Shutdown completed")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://frontend:80",    # Для запросов внутри Docker-сети
        "http://localhost:8080"], # Для запросов из браузера],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
for router in routers:
    app.include_router(router)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}
