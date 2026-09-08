from sqlalchemy import Select
from sqlalchemy.orm import DeclarativeBase

from app.repository.base import HasId
from app.specification.base import BaseWhereSpecification


class RepositoryWhereFilterMixin:


	def filter_by_specs[S: BaseWhereSpecification, T:(DeclarativeBase, HasId)](self, query: Select[T], specs: S, filters_map=None) -> Select[T]:

		if filters_map is None:
			filters_map = self._where_filters_map.copy()
		else:
			filters_map = filters_map.copy()

		parent_filters_map = super()._where_filters_map.copy() # copy of parent's map.

		parent_filters_map.update(filters_map) # merging our filters with parent's filter

		filters_map = parent_filters_map  # fully updated filters map.

		return super().filter_by_specs(query, specs, filters_map=filters_map)

