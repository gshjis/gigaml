from fastapi import APIRouter

router = APIRouter(prefix='/ping', tags=['ping'])

@router.get('/db')
async def ping():
    return {'message': 'Ping DB ok.'}

@router.get('/app')
async def ping():
    return {'message': 'Ping app ok.'}