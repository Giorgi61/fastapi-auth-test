from pydantic import BaseModel

from app.repository.users import UserRepository
from app.schemas.services.users import UserServiceSchema
from app.service.base import BaseService
from app.service.protocols import PasswordHasherProtocol


class UserService[Repo: UserRepository, CanHash: PasswordHasherProtocol](BaseService):
	PModel = BaseModel
	PSchema = type[UserServiceSchema]

	_schema = UserServiceSchema


	def __init__(self, repo: Repo, hasher: CanHash) -> None:
		super().__init__(repo)
		self._hasher = hasher


	async def create_user(self, data: dict):

		password = data.pop('password')

		hashed_password = self._hasher.hash_password(password)

		data['hashed_password'] = hashed_password

		return await self.create(data)



