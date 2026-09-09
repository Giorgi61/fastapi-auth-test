from fastapi import APIRouter

from app.api.users import router as user_router
from app.api.posts import router as post_router

routers = APIRouter()

routers.include_router(user_router, prefix="/users", tags=["users"])
routers.include_router(post_router, prefix="/posts", tags=["posts"])