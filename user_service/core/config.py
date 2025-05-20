from functools import lru_cache
from typing import Optional
from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Basic App Info
    PROJECT_NAME: str = "User Service"
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG_MODE: bool = Field(default=False, env="DEBUG_MODE")

    # App Host/Port
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database
    DATABASE_URL: str

    # JWT / Auth
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # SMTP / Email (optional)
    SMTP_SERVER: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None

    # Logging
    LOG_LEVEL: str = "INFO"
    SENSITIVE_KEYS: list[str] = Field(default=["password", "secret", "token", "access_token", "refresh_token", "email", "ssn", "authorization"])

    # Model Config (important for env + strict fields)
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="forbid" 
    )

    @validator("ENVIRONMENT")
    def validate_env(cls, v):
        allowed = ("development", "production", "testing")
        if v not in allowed:
            raise ValueError(f"ENVIRONMENT must be one of: {', '.join(allowed)}")
        return v


@lru_cache()
def get_settings() -> Settings:
    return Settings()
