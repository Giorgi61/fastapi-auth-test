from app.schemas.api.posts import PostResponse, PostWitIdResponse
from app.schemas.api.users import UserResponse, UserResponseWithId


class UserResponseWithPost(UserResponse):

	posts: list[PostResponse]



class UserResponseWithPostId(UserResponseWithId):
	posts: list[PostWitIdResponse]



class PostResponseWithUser(PostResponse):

	author: UserResponse



class PostWitIdResponseWithUserId(PostWitIdResponse):

	author: UserResponseWithId