from app.schemas.services.user_post_common import PostUserServiceSchema
from app.service.base import BaseService
from app.repository.posts import PostRepository

class PostService[Repo: PostRepository](BaseService):

	PSchema = type[PostUserServiceSchema]

	_schema: PSchema = PostUserServiceSchema