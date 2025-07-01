from fastapi import APIRouter

router = APIRouter(prefix="/ping", tags=["ping"])


@router.get("/db")
async def ping_db():
    return {"message": "Ping DB ok."}


@router.get("/app")
async def ping_app():
    return {"message": "Ping app ok."}
