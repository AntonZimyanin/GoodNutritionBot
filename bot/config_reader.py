import os
from enum import Enum
from typing import Optional

from pydantic import BaseModel
from pydantic import BaseSettings
from pydantic import RedisDsn
from pydantic import SecretStr


class FSMModeEnum(str, Enum):
    MEMORY = "memory"
    REDIS = "redis"


class Redis(BaseModel):
    dsn: RedisDsn  # Without database id!
    fsm_db_id: int
    data_db_id: int


class Settings(BaseSettings):
    bot_token: SecretStr
    db_url: str
    redis: Optional[Redis]
    fsm_mode: FSMModeEnum

    class Config:
        env_file = f"{os.path.dirname(os.path.abspath(__name__))}\\.env"
        env_file_encoding = "utf-8"


config = Settings()
