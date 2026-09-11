from app.specification.users import UserLoadSpecification
from app.repository.users import UserRepository
from app.schemas.services.user_post_common import UserPostServiceSchema
from app.service.base import BaseService
from app.service.protocols import PasswordHasherProtocol


class UserService[Repo: UserRepository, CanHash: PasswordHasherProtocol](BaseService):

	PSchema = type[UserPostServiceSchema]

	_schema: PSchema = UserPostServiceSchema


	def __init__(self, repo: Repo, hasher: CanHash) -> None:
		super().__init__(repo)
		self._hasher = hasher


	async def create_user(self, data: dict) -> PSchema:

		password = data.pop('password')

		hashed_password = self._hasher.hash_password(password)

		data['hashed_password'] = hashed_password

		return await self.create(data)


	async def get_user(self, user_id: int, relationships: bool = False) -> PSchema:

		if relationships:
			lspec = UserLoadSpecification()
		else:
			lspec = None

		return await self.select_one(user_id, lspec)






