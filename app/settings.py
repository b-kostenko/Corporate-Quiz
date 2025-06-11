from pydantic_settings import BaseSettings, SettingsConfigDict


class TokenSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    TOKEN_TYPE: str
    model_config = SettingsConfigDict(env_file=".env", env_prefix="JWT_", extra="ignore")


class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    DATABASE_URL: str
    token: TokenSettings = TokenSettings()
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
