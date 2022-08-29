
from typing import Any, Dict, Optional

from pydantic import BaseSettings, PostgresDsn, validator

from datetime import datetime


class Settings(BaseSettings):
    PROJECT_NAME: str

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    DATABASE_URI: Optional[PostgresDsn] = None

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get('POSTGRES_PORT'),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    BOT_TOKEN: str
    BOT_WEB_HOOK_URL: str
    TIMER: datetime
    TZ_OFFSET: int

    class Config:
        case_sensitive = True
        env_file = '.env'


settings = Settings()
