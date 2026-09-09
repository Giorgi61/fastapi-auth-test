from collections.abc import Sequence
from typing import Protocol

from sqlalchemy import Select, select, Result
from sqlalchemy import delete as sa_delete
from sqlalchemy.ext.asyncio import  AsyncSession
from sqlalchemy.orm import DeclarativeBase, joinedload, selectinload

from app.specification.base import BaseWhereSpecification


class HasId(Protocol):
	id: int


class BaseRepository[T: type[DeclarativeBase, HasId], S: BaseWhereSpecification, D: dict]:
	__tablename__ = "base"

	_selectin_relationships: list[str] = []
	_joined_relationships: list[str] = []
	_where_filters_map = {"id_eq": lambda model, val: model.id == val,
	                      "created_at_gt": lambda model, val: model.created_at > val,
	                      "created_at_lt": lambda model, val: model.created_at < val,
	                      "updated_at_gt": lambda model, val: model.updated_at > val,
	                      "updated_at_lt": lambda model, val: model.updated_at < val
	                      }

	def __init__(self, session: AsyncSession, model: T) -> None:
		self._session = session
		self._model = model

	def select_related(self, query: Select[T]) -> Select[T]:
		if self._selectin_relationships:
			for rel in self._selectin_relationships:
				rel_field = getattr(self._model, rel)
				query = query.options(selectinload(rel_field))

		return query

	def join_related(self, query: Select[T]) -> Select[T]:
		if self._joined_relationships:

			for joined_rel in self._joined_relationships:
				joined_field = getattr(self._model, joined_rel)
				query = query.options(joinedload(joined_field))

		return query

	def load_all(self, query: Select[T]) -> Select[T]:

		query = self.select_related(query)
		query = self.join_related(query)

		return query

	async def _refresh_obj(self, orm_object: T) -> None:
		await self._session.refresh(orm_object,
		                            attribute_names=self._selectin_relationships + self._joined_relationships)


	def filter_by_specs(self, query: Select[T], specs: S, filters_map=None) -> Select[T]:
		if not filters_map:
			filters_map = self._where_filters_map

		specs_dict = specs.model_dump(exclude_none=True)

		for specs_name, val in specs_dict.items():
			if specs_name in filters_map:
				query_filter = filters_map[specs_name](self._model, val)

				query = query.where(query_filter)

		return query


	async def _select(self, *, specs: S | None = None, skip: int =0, total: int =0) -> Result:

		query = select(self._model)

		if specs is not None:
			query = self.filter_by_specs(query, specs)

		query = self.load_all(query)

		query = query.offset(skip)

		if total:
			limit = skip + total
			query = query.limit(limit)

		return await self._session.execute(query)



	async def select_model(self, *, specs: S | None = None, skip: int =0, total: int =0 ) -> Sequence[T]:


		res =  await self._select(specs=specs, skip=skip, total=total)

		return res.scalars().all()

	async def select_one(self, specs: S | None = None ):

		res = await self._select(specs=specs, total=1)
		return res.scalar()

	async def create(self, items: D) -> T:

		orm_object = self._model(**items)

		self._session.add(orm_object)
		await self._session.commit()


		return orm_object.id

	async def update_obj(self, id_: int, data: D) -> T:

		orm_object = await self._session.get(self._model, id_)

		for attr, value in data.items():
			setattr(orm_object, attr, value)

		await self._session.commit()
		return orm_object




	async def delete_obj(self, _id: int) -> int | None:

		stmt = (sa_delete(self._model).
		        where(self._model.id == _id).
		        returning(self._model.id))


		res =  await self._session.scalar(stmt)

		await self._session.commit()

		return res