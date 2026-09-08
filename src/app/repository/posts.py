from app.models.posts import Post
from app.repository.base import BaseRepository, HasId
from app.repository.mixins import RepositoryWhereFilterMixin
from app.specification.posts import PostWhereSpecification


class PostRepository[T: type[Post, HasId], S: PostWhereSpecification](RepositoryWhereFilterMixin, BaseRepository):

	_joined_relationships: list[str] = ["author"]