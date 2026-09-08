from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings
from app.models.base import Base


class AsyncDB:
    def __init__(self, db_url: str, orm: type[DeclarativeBase] = Base):

        self._engine = create_async_engine(db_url)

        self._session_factory = async_sessionmaker(self._engine,
                                                   class_=AsyncSession,
                                                   autoflush=False,
                                                   expire_on_commit=False, )

        self._orm = orm

    @asynccontextmanager
    async def create_database_lifespan(self, _app: FastAPI):
        async with self._engine.begin() as conn:
            await conn.run_sync(self._orm.metadata.create_all)

        yield

        await self._engine.dispose()

    async def get_session(self) -> AsyncIterator[AsyncSession]:
        async with self._session_factory() as session:
            yield session

db = AsyncDB(settings.DB_URI)