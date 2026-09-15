
from fastapi import APIRouter

from app.api.dependencies import PService
from app.schemas.api.posts import CreatePost, PostWitIdResponse

router = APIRouter()



@router.get('', response_model=list[PostWitIdResponse])
async def get_all_posts(post_serv: PService, skip: int = 0, total: int=0):

	return await post_serv.select_all(skip=skip, total=total)


@router.post('', response_model=PostWitIdResponse)
async def create_post(data: CreatePost, post_serv: PService):

	data_dict = data.model_dump()
	return await post_serv.create(data_dict)

