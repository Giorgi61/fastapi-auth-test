from __future__ import annotations

from typing import TYPE_CHECKING

from app.schemas.common_constraints import nullable_str, str200
from app.schemas.services.base import BaseServiceSchema




class PostServiceSchema(BaseServiceSchema):

	title: str200
	content: nullable_str
	user_id: int


