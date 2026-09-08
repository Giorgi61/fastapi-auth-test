from fastapi import APIRouter

from app.api.users import router as user_router

routers = APIRouter()

routers.include_router(user_router, prefix="/users", tags=["users"])
