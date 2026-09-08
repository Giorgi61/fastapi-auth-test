from pydantic import BaseModel

from app.repository.base import BaseRepository
from app.schemas.services.base import BaseServiceSchema


class BaseService[Repo: BaseRepository, PModel: BaseModel, PSchema: BaseServiceSchema]:

	_schema: PSchema =  type[PSchema]

	def __init__(self, repo: Repo,  ) -> None:
		self._repo = repo




	async def create(self, items: dict) -> PSchema:


		obj = await self._repo.create(items)
		return self._schema.model_validate(obj)

	async def select_all(self) -> list[PSchema]:

		res = await self._repo.select_model()

		return [self._schema.model_validate(item) for item in res]


	async def delete_ojb(self, _id: int) -> int | None:

		return await self._repo.delete_obj(_id)



