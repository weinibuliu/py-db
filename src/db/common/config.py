import urllib.parse
from pathlib import Path
from typing import Optional

import dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

ENV_FILE_PATH = Path.cwd() / ".env"

dotenv.load_dotenv(ENV_FILE_PATH)


class DBConfig(BaseSettings):
    host: str = Field(default=...)
    port: int = Field(default=...)
    name: str = Field(default=...)
    user: str = Field(default=...)
    password: str = Field(default=...)

    @property
    def url(self) -> str:
        return f"mysql+pymysql://{self.user}:{urllib.parse.quote_plus(self.password)}@{self.host}:{self.port}/{self.name}"

    model_config = {
        "env_prefix": "DB_",
        "case_sensitive": False,
        "extra": "ignore",
        "validate_default": False,
    }


class RedisConfig(BaseSettings):
    host: str = Field(default=...)
    port: int = Field(default=...)
    user: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default=None)

    model_config = {
        "env_prefix": "REDIS_",
        "case_sensitive": False,
        "extra": "ignore",
        "validate_default": False,
    }
