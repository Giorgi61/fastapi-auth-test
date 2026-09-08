
from app.specification.base import BaseWhereSpecification


class UsersWhereSpecification(BaseWhereSpecification):

	email_ilike: str | None = None
	first_name_ilike: str | None = None
	last_name_ilike: str | None = None
