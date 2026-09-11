from typing import Annotated

from fastapi import APIRouter, Depends

from app.service.dependencies import get_post_service
from app.service.posts import PostService

router = APIRouter()

PService =  Annotated[PostService, Depends(get_post_service)]


@router.get('')
async def get_all_posts(post_serv: PService, skip: int = 0, total: int=0):

	return await post_serv.select_all(skip=skip, total=total)