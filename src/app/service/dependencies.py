from typing import Annotated

from fastapi import Depends

from app.core.security import PasswordHasher
from app.repository.dependencies import get_users_repo
from app.repository.users import UserRepository
from app.service.users import UserService

UserRepo=Annotated[UserRepository, Depends(get_users_repo)]

def get_user_service( repo: UserRepo, hasher = PasswordHasher
) -> UserService[UserRepo, PasswordHasher]:
    return UserService(repo, hasher)