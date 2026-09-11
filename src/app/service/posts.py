from app.repository.posts import PostRepository
from app.schemas.services.user_post_common import PostUserServiceSchema
from app.service.base import BaseService


class PostService[Repo: PostRepository](BaseService):

	PSchema = type[PostUserServiceSchema]

	_schema: PSchema = PostUserServiceSchema