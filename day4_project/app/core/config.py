from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME:    str = "Day 4 — SQLAlchemy + PostgreSQL"
    APP_VERSION: str = "4.0.0"
    DEBUG:       bool = True

    # ── PostgreSQL connection ─────────────────────────────
    DB_HOST:     str = "localhost"
    DB_PORT:     int = 5433
    DB_NAME:     str = "day4_db"
    DB_USER:     str = "postgres"
    DB_PASSWORD: str = "1234"

    @property
    def DATABASE_URL(self) -> str:
        """Async URL for SQLAlchemy (asyncpg driver)."""
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def DATABASE_URL_SYNC(self) -> str:
        """Sync URL for Alembic migrations (psycopg2 driver)."""
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
