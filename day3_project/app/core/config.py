# =============================================================
#  app/core/config.py  —  TOPIC: Config Injection
# =============================================================

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME:          str  = "Day 3 FastAPI Training"
    APP_VERSION:       str  = "3.0.0"
    DEBUG:             bool = True
    DEFAULT_PAGE_SIZE: int  = 10
    MAX_PAGE_SIZE:     int  = 100
    DB_TYPE:           str  = "fake"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    """
    TOPIC: Config Injection
    @lru_cache → Settings() created only ONCE, reused every request.
    Override in tests: app.dependency_overrides[get_settings] = lambda: TestSettings()
    """
    return Settings()
