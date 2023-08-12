from fastapi import APIRouter

from apis.v1.endpoints import parking, user


api_router = APIRouter()

api_router.include_router(parking.router, prefix='/parkings', tags=['parkings'])
api_router.include_router(user.router, prefix='/users', tags=['users'])
