from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str
    redis_url: str = "redis://redis:6379/0"
    deribit_api_url: str = "https://www.deribit.com/api/v2"
    celery_broker_url: str = "redis://redis:6379/0"
    celery_result_backend: str = "redis://redis:6379/0"
    debug: bool = True
    secret_key: str = "your-secret-key-change-this-in-production"

    class Config:
        env_file = ".env"
        extra = "ignore"  # This allows extra env vars without validation errors


@lru_cache()
def get_settings() -> Settings:
    return Settings()