from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class TokenSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    TOKEN_TYPE: str
    model_config = SettingsConfigDict(env_file=".env", env_prefix="JWT_", extra="ignore")


class CelerySettings(BaseSettings):
    # Celery
    broker_db: int = Field(0, alias="CELERY_BROKER_DB")
    backend_db: int = Field(1, alias="CELERY_BACKEND_DB")
    celery_broker: str = Field("", alias="CELERY_BROKER_URL")
    celery_backend: str = Field("", alias="CELERY_RESULT_BACKEND")
    model_config = SettingsConfigDict(env_file=".env", env_prefix="CELERY_", extra="ignore")

class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    DATABASE_URL: str
    token: TokenSettings = TokenSettings()
    celery: CelerySettings = CelerySettings()
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
