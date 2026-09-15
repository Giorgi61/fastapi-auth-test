from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from app.core.config import settings


class PasswordHasher:
	pwd_hash = PasswordHash.recommended()

	@classmethod
	def hash_password(cls, password: str) -> str:
		return cls.pwd_hash.hash(password)

	@classmethod
	def verify_password(cls, password: str, hashed_password: str) -> bool:
		return cls.pwd_hash.verify(password, hashed_password)


class TokenFactory:

	@staticmethod
	def create_access_token(data: dict, expires_delta: timedelta | None = None):
		to_encode = data.copy()
		if expires_delta:
			expire = datetime.now(UTC) + expires_delta
		else:
			expire = datetime.now(UTC) + timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
		to_encode.update({"exp": expire})
		encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY.get_secret_value(), algorithm=settings.ALGORITHM)
		return encoded_jwt

	@staticmethod
	def verify_token(token: str) -> dict | bool:

		try:
			payload = jwt.decode(token, settings.SECRET_KEY.get_secret_value(), algorithms=settings.ALGORITHM)

		except jwt.InvalidTokenError:

			return False

		else:
			return payload
