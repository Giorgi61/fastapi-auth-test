from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, Str50, Str200

if TYPE_CHECKING:

    from app.models.posts import Post


class User(Base):
    __tablename__ = "users"

    name: Mapped[Str50]
    lastname: Mapped[Str50]
    email: Mapped[Str50] = mapped_column(unique=True)
    hashed_password: Mapped[Str200]

    posts: Mapped[list[Post]] = relationship(
        "Post", back_populates="author", cascade="all, delete-orphan"
    )
