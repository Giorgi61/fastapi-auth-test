from typing import Protocol
from pydantic import BaseModel
from datetime import timedelta


class PasswordHasherProtocol(Protocol):

	@classmethod
	def hash_password(cls, password: str) -> str:
		pass

	@classmethod
	def verify_password(cls, password: str, hashed_password: str) -> bool:
		pass


class UserServiceProtocol(Protocol):

	async def find_by_mail(self, mail) -> type[BaseModel] | None:
		pass

	async def select_one(self, id_: int) -> type[BaseModel] | None:
		pass


class TokenServiceProtocol(Protocol):

	@staticmethod
	def create_access_token(data: dict, expires_delta: timedelta | None = None):
		pass

	@staticmethod
	def verify_token(token: str) -> dict | bool:
		pass
