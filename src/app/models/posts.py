from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, Str200

if TYPE_CHECKING:

    from app.models.users import User


class Post(Base):
    __tablename__ = "posts"

    title: Mapped[Str200]
    content: Mapped[str]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

    author: Mapped[User] = relationship("User", back_populates="posts", lazy="noload")
