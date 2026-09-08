from pydantic import BaseModel, EmailStr

from app.schemas.api.base import BaseResponse, BaseResponseWitId
from app.schemas.common_constraints import password_field, str50


class UserCreate(BaseModel):
	name: str50
	lastname: str50
	email: EmailStr
	password: password_field


class UserUpdate(BaseModel):
	name: str50
	lastname: str50
	password: password_field | None = None



class UserResponse(BaseResponse):

	name: str50
	lastname: str50
	email: EmailStr


class UserResponseWithId(BaseResponseWitId):
	name: str50
	lastname: str50
	email: EmailStr



