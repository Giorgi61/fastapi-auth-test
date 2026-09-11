from datetime import datetime

from pydantic import BaseModel


class BaseWhereSpecification(BaseModel):

	id_eq: int | None = None

	created_at_gt: datetime | None = None
	created_at_lt: datetime | None = None

	updated_at_gt: datetime | None = None
	updated_at_lt: datetime | None = None


class BaseLoadSpecification(BaseModel):

	selectinload: list[str] = []
	joinedload: list[str] = []
