from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class SMTPSettings(BaseSettings):
    SMTP_EMAIL_HOST: str = Field(..., alias="SMTP_EMAIL_HOST")
    SMTP_EMAIL_PORT: int = Field(..., alias="SMTP_EMAIL_PORT")
    SMTP_EMAIL_USERNAME: str = Field(..., alias="SMTP_EMAIL_USERNAME")
    SMTP_EMAIL_PASSWORD: str = Field(..., alias="SMTP_EMAIL_PASSWORD")
    SMTP_FROM_EMAIL: str = Field(..., alias="SMTP_FROM_EMAIL")

    model_config = SettingsConfigDict(env_file=".env", env_prefix="SMTP_", extra="ignore")

class GoogleSSOSettings(BaseSettings):
    GOOGLE_CLIENT_ID: str = Field(..., alias="GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = Field(..., alias="GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI: str = Field(default="http://localhost:8000/auth/google/callback", alias="GOOGLE_REDIRECT_URI")
    GOOGLE_AUTHORITY: str = Field(default="https://accounts.google.com", alias="GOOGLE_AUTHORITY")
    GOOGLE_SCOPES: list[str] = ["openid", "email", "profile"]

    model_config = SettingsConfigDict(env_file=".env", env_prefix="GOOGLE_", extra="ignore")

class AzureSSOSettings(BaseSettings):
    AZURE_CLIENT_ID: str = Field(..., alias="AZURE_CLIENT_ID")
    AZURE_TENANT_ID: str = Field(..., alias="AZURE_TENANT_ID")
    AZURE_CLIENT_SECRET: str = Field(..., alias="AZURE_CLIENT_SECRET")
    AZURE_REDIRECT_URI: str = Field(default="http://localhost:8000/auth/azure/callback", alias="AZURE_REDIRECT_URI")
    AZURE_AUTHORITY: str = Field(default="https://login.microsoftonline.com", alias="AZURE_AUTHORITY")
    AZURE_SCOPES: list[str] = ["openid", "email", "profile"]

    model_config = SettingsConfigDict(env_file=".env", env_prefix="AZURE_", extra="ignore")


class TokenSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    RESET_PASSWORD_TOKEN_EXPIRE_MINUTES: int
    TOKEN_TYPE: str

    model_config = SettingsConfigDict(env_file=".env", env_prefix="JWT_", extra="ignore")


class CelerySettings(BaseSettings):
    # Celery
    broker_db: int = Field(0, alias="CELERY_BROKER_DB")
    backend_db: int = Field(1, alias="CELERY_BACKEND_DB")
    celery_broker: str = Field("", alias="CELERY_BROKER_URL")
    celery_backend: str = Field("", alias="CELERY_RESULT_BACKEND")
    model_config = SettingsConfigDict(env_file=".env", env_prefix="CELERY_", extra="ignore")


class FileStorageSettings(BaseSettings):
    """Settings for file storage configuration."""

    base_path: Path = Field(default=Path("media"), alias="STORAGE_BASE_PATH")
    base_url: str = Field(default="http://localhost:8000", alias="STORAGE_BASE_URL")
    allowed_extensions: list[str] = Field(default=[".jpg", ".jpeg", ".png", ".gif", ".webp"], alias="STORAGE_ALLOWED_EXTENSIONS")
    max_file_size: int = Field(default=10 * 1024 * 1024, alias="STORAGE_MAX_FILE_SIZE")  # 10MB
    model_config = SettingsConfigDict(env_file=".env", env_prefix="STORAGE_", extra="ignore")

class RedisSettings(BaseSettings):
    REDIS_HOST: str = Field(..., alias="REDIS_HOST")
    REDIS_PORT: int = Field(..., alias="REDIS_PORT")
    REDIS_DB: int = Field(0, alias="REDIS_DB")
    REDIS_DB_QUIZ_ANSWERS: int = Field(0, alias="REDIS_DB_QUIZ_ANSWERS")
    REDIS_PASSWORD: str | None = Field(None, alias="REDIS_PASSWORD")

    model_config = SettingsConfigDict(env_file=".env", env_prefix="REDIS_", extra="ignore")

class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    BASE_URL: str = Field(default="http://localhost:8000", alias="BASE_URL")
    DATABASE_URL: str
    TEMPLATES_DIR: Path = Path("app/templates")


    token: TokenSettings = TokenSettings()
    celery: CelerySettings = CelerySettings()
    file_storage: FileStorageSettings = FileStorageSettings()
    azure_sso: AzureSSOSettings = AzureSSOSettings()
    google_sso: GoogleSSOSettings = GoogleSSOSettings()
    smtp: SMTPSettings = SMTPSettings()
    redis: RedisSettings = RedisSettings()
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
