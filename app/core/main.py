from fastapi import FastAPI

from app.core.settings import settings
from app.handlers import routers

app = FastAPI()


@app.get("/ping")
async def ping():
    return {"message": settings.GOOGLE_TOKEN_ID}


for router in routers:
    app.include_router(router)
