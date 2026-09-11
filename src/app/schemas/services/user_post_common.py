from app.schemas.services.posts import PostServiceSchema
from app.schemas.services.users import UserServiceSchema


class UserPostServiceSchema(UserServiceSchema):

	posts: list[PostServiceSchema] | None = None

class PostUserServiceSchema(PostServiceSchema):

	author: UserServiceSchema | None = None
