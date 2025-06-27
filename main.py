from fastapi import FastAPI
from handlers import routers

app = FastAPI()

@app.get('/')
async def main():
    return {'message': 'Ok'}

for router in routers:
    app.include_router(router)