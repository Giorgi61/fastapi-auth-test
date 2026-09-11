
from app.models.users import User
from app.repository.base import BaseRepository
from app.repository.mixins import HasId, RepositoryWhereFilterMixin
from app.specification.users import UsersWhereSpecification


class UserRepository[T: type[User, HasId], S: UsersWhereSpecification](RepositoryWhereFilterMixin, BaseRepository):




	_selectin_relationships: list[str] = ['posts']

	_where_filters_map = {"email_ilike": lambda model, val: model.email.ilike(val),
	                      "first_name_ilike": lambda model, val: model.name.ilike(val),
	                      "last_name_ilike": lambda model, val: model.lastname.ilike(val),
	                      }


	async def select_paginated_posts(self, ):
		pass