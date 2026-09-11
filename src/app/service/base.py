
from app.repository.base import BaseRepository
from app.schemas.services.base import BaseServiceSchema
from app.specification.base import BaseLoadSpecification, BaseWhereSpecification


class BaseService[Repo: BaseRepository, PSchema: BaseServiceSchema]:

	_schema: PSchema =  type[PSchema]

	def __init__(self, repo: Repo,  ) -> None:
		self._repo = repo



	async def select_one(self, id_: int, lspec: BaseLoadSpecification | None = None) -> PSchema:

		wspec = BaseWhereSpecification(id_eq=id_)
		return await self._repo.select_one(wspec=wspec, lspec=lspec)

	async def select_all(self, lspec: BaseLoadSpecification | None = None, skip: int=0, total: int=0) -> list[PSchema]:

		res = await self._repo.select_model(skip=skip, total=total)

		return [self._schema.model_validate(item) for item in res]


	async def delete_ojb(self, _id: int) -> int | None:

		return await self._repo.delete_obj(_id)



	async def update(self, _id: int, data: dict) -> PSchema:

		await self._repo.update_obj(_id, data)

		obj = await self.select_one(_id)

		# return self._schema.model_validate(obj)
		return obj

	async def create(self, items: dict) -> PSchema:


		id_ = await self._repo.create(items)

		obj = await self.select_one(id_)

		return self._schema.model_validate(obj)

