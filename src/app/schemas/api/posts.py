from pydantic import BaseModel

from app.schemas.api.base import BaseResponse, BaseResponseWitId
from app.schemas.common_constraints import nullable_str, str200


class CreatePost(BaseModel):

	title: str200
	content: nullable_str
	user_id: int


class PostResponse(BaseResponse):

	title: str200
	content: nullable_str



class PostWitIdResponse(BaseResponseWitId):
	title: str200
	content: nullable_str

