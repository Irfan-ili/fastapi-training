from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from core.config import get_settings

settings = get_settings()

# ── 1. Engine ─────────────────────────────────────────────────
# Creates the connection pool to PostgreSQL.
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,   # set to False in production
    pool_size=5,
    max_overflow=10,
)

# ── 2. Session factory ────────────────────────────────────────
# AsyncSession is the async version of SQLAlchemy's Session.
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# ── 3. Base class ─────────────────────────────────────────────
# All ORM models inherit from Base.
class Base(DeclarativeBase):
    pass
