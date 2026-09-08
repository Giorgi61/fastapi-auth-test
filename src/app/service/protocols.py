from typing import Protocol


class PasswordHasherProtocol(Protocol):

	@classmethod
	def hash_password(cls, password: str) -> str:
		pass

	@classmethod
	def verify_password(cls, password: str, hashed_password: str) -> bool:
		pass

