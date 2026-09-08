from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import db
from app.models.posts import Post
from app.models.users import User
from app.repository.posts import PostRepository
from app.repository.users import UserRepository

AsyncDBSession = Annotated[AsyncSession, Depends(db.get_session)]

def get_users_repo(session: AsyncDBSession):

	return UserRepository(session, User)


def get_posts_repo(session: AsyncDBSession):

	return PostRepository(session, Post)