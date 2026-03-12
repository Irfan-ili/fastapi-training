from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from database.base import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session          # route runs here
            await session.commit() # auto-commit on success
        except Exception:
            await session.rollback() # rollback on error
            raise
