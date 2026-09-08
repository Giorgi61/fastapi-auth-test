from app.schemas.services.users import UserServiceSchema
from app.schemas.services.posts import PostServiceSchema,


class UserPostServiceSchema(UserServiceSchema):

	posts: list[PostInUserServiceSchema]

class PostUserServiceSchema(PostServiceSchema):

	author: UserServiceSchema