from fastapi import APIRouter

from app.api.endpoints import devices

api_router = APIRouter()
api_router.include_router(devices.router, tags=["devices"])