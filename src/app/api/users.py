from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import status

from app.service.dependencies import get_user_service
from app.service.users import UserService

from app.schemas.api.users import UserCreate
router = APIRouter()

UService =  Annotated[UserService, Depends(get_user_service)]

@router.get("", )
async def get_all_users(user_serv: UService):

    return await user_serv.select_all()

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(user_info: UserCreate, user_serv: UService):

    data = user_info.model_dump()
    return await user_serv.create_user(data)
