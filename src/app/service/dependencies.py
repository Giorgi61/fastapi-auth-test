from typing import Annotated

from fastapi import Depends

from app.core.security import PasswordHasher
from app.repository.dependencies import get_posts_repo, get_users_repo
from app.repository.posts import PostRepository
from app.repository.users import UserRepository
from app.service.posts import PostService
from app.service.users import UserService

UserRepo = Annotated[UserRepository, Depends(get_users_repo)]
PostRepo = Annotated[PostRepository, Depends(get_posts_repo)]
HasherCls = Annotated[PasswordHasher, Depends(PasswordHasher)]


def get_user_service(repo: UserRepo, hasher: HasherCls) -> UserService[UserRepo, PasswordHasher]:
	return UserService(repo, hasher)


def get_post_service(repo: PostRepo) -> PostService[PostRepo]:
	return PostService(repo)
