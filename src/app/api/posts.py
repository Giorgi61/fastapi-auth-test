from typing import Annotated

from fastapi import APIRouter, Depends

from app.service.dependencies import get_post_service
from app.service.posts import PostService
from app.schemas.api.posts import PostWitIdResponse, CreatePost
router = APIRouter()

PService =  Annotated[PostService, Depends(get_post_service)]


@router.get('', response_model=PostWitIdResponse)
async def get_all_posts(post_serv: PService, skip: int = 0, total: int=0):

	return await post_serv.select_all(skip=skip, total=total)


@router.post('', response_model=PostWitIdResponse)
async def create_post(data: CreatePost, post_serv: PService):

	data_dict = data.model_dump()
	return await post_serv.create(data_dict)

