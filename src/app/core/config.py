from pathlib import Path

from pydantic import SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.utils import get_project_root

ROOT_DIR = get_project_root()

class Settings(BaseSettings):
	model_config = SettingsConfigDict(
		env_file=str(ROOT_DIR / ".env"),
		env_file_encoding="utf-8")

	PROJECT_ROOT: str | Path = ROOT_DIR

	ALGORITHM: str = "HS256"
	ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

	SECRET_KEY: SecretStr

	DB_PARAMS: str
	DB_NAME: str = 'test.db'

	DB_URI: str | None  = None

	@model_validator(mode='after')
	def create_db_uri(self):

		self.DB_URI = f'{self.DB_PARAMS}/{self.PROJECT_ROOT}/{self.DB_NAME}'

		return self


settings = Settings()
