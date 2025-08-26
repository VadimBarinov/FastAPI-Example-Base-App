from pydantic import (
    BaseModel,
    PostgresDsn
)
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from pathlib import Path

BASE_URL = Path(__file__).parent.parent


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080


class ApiPrefix(BaseModel):
    prefix: str = "/api"


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 50
    pool_size: int = 10


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(BASE_URL / ".env.template", BASE_URL / ".env"),
        # Не важен регистр
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig


settings = Settings()
