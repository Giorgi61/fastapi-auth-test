from __future__ import annotations

from pydantic import EmailStr

from app.schemas.common_constraints import str50, str200
from app.schemas.services.base import BaseServiceSchema


class UserServiceSchema(BaseServiceSchema):

	name: str50
	lastname:  str50
	email: EmailStr
	hashed_password: str200




