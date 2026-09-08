from __future__ import annotations



from typing import Annotated

from pydantic import (
	BaseModel,
	EmailStr,
	Field,

)

from app.schemas.api.base import BaseResponse, BaseResponseWitId
from app.schemas.common_constraints import str50

class UserCreate(BaseModel):
	name: str50
	lastname: str50
	email: EmailStr
	password: Annotated[str, Field(min_length=8,)]




class UserResponse(BaseResponse):

	name: str50
	lastname: str50
	email: EmailStr


class UserResponseWithId(BaseResponseWitId):
	name: str50
	lastname: str50
	email: EmailStr



