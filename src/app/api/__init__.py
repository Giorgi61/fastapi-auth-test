from fastapi import APIRouter

from app.api.posts import router as post_router
from app.api.users import router as user_router

routers = APIRouter()

routers.include_router(user_router, prefix="/users", tags=["users"])
routers.include_router(post_router, prefix="/posts", tags=["posts"])