from pathlib import Path

from pydantic import SecretStr, field_validator
from pydantic.functional_validators import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.utils import get_project_root

ROOT_DIR = get_project_root()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ROOT_DIR / ".env"), env_file_encoding="utf-8"
    )

    PROJECT_ROOT: str | Path = ROOT_DIR

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    SECRET_KEY: SecretStr

    DB_DRIVER: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    DB_URL: str | None = None

    OAUTH_SECRET_KEY: SecretStr
    GOOGLE_CLIENT_ID: SecretStr
    GOOGLE_CLIENT_SECRET: SecretStr

    GOOGLE_SERVER_METADATA_URL: str
    GOOGLE_SCOPE: str = "openid email profile"

    @field_validator("GOOGLE_SCOPE", mode="after")
    @classmethod
    def strip_scope(cls, scope) -> str:
        print(scope)
        return scope.strip('"')
        print(scope)

    @model_validator(mode="after")
    def build_db_url(self) -> Settings:
        self.DB_URL = f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

        return self


settings = Settings()
