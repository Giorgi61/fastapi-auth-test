from datetime import timedelta
from typing import Protocol

from pydantic import BaseModel


class PasswordHasherProtocol(Protocol):

	@classmethod
	def hash_password(cls, password: str) -> str:
		pass

	@classmethod
	def verify_password(cls, password: str, hashed_password: str) -> bool:
		pass

	@classmethod
	def generate_random_password(cls) -> str:
		pass


class UserServiceProtocol(Protocol):

	async def find_by_mail(self, mail) -> BaseModel | None:
		pass

	async def select_one(self, id_: int) -> BaseModel | None:
		pass

	async def create_user(self, data: dict) -> BaseModel:
		pass

class TokenServiceProtocol(Protocol):

	@staticmethod
	def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
		pass

	@staticmethod
	def verify_token(token: str) -> dict | bool:
		pass
