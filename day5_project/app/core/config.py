from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME:    str = "Day 5 — OAuth2 + JWT"
    APP_VERSION: str = "5.0.0"
    DEBUG:       bool = True

    # ── Database ──────────────────────────────────────────────
    DB_HOST:     str = "localhost"
    DB_PORT:     int = 5433
    DB_NAME:     str = "day5_db"
    DB_USER:     str = "postgres"
    DB_PASSWORD: str = "1234"

    # ── JWT Settings ──────────────────────────────────────────
    SECRET_KEY:            str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM:             str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30   # token valid for 30 mins

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def DATABASE_URL_SYNC(self) -> str:
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
