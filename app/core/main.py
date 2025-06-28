from fastapi import FastAPI
from app.core.settings import Settings
from app.handlers import routers
from app.core.database import get_db_connection

settings = Settings()
app = FastAPI()

@app.get('/ping')
async def ping():
    return {'message': settings.GOOGLE_TOKEN_ID}


for router in routers:
    app.include_router(router)