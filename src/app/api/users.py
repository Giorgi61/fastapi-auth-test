from typing import Annotated

from fastapi import APIRouter, Depends, status
from starlette.exceptions import HTTPException

from app.schemas.api.users import UserCreate, UserResponseWithId, UserUpdate
from app.schemas.api.user_post_common import UserResponseWithPostId
from app.service.dependencies import get_user_service
from app.service.users import UserService

router = APIRouter()

UService =  Annotated[UserService, Depends(get_user_service)]

@router.get("", response_model=list[UserResponseWithId])
async def get_all_users(user_serv: UService, skip: int=0, total: int=0 ):

    return await user_serv.select_all(skip, total)


@router.get("/{u_id}", response_model=UserResponseWithId)
async def get_user(u_id: int, user_serv: UService):
    return await user_serv.select_one(u_id)


@router.get('/{u_id}/posts', response_model=UserResponseWithPostId)
async def get_user_with_post(u_id: int, user_serv: UService):
    return await user_serv.select_one(u_id)

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(user_info: UserCreate, user_serv: UService):

    data = user_info.model_dump()
    try:
        return await user_serv.create_user(data)

    except Exception:

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Unmeted requirements!')


@router.patch("/{u_id}", status_code=status.HTTP_200_OK, response_model=UserResponseWithId)
async def update_user(u_id: int, user_serv: UService, data: UserUpdate):

    to_update = data.model_dump(exclude_unset=True)

    return await user_serv.update(u_id, to_update)