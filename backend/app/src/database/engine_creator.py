from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config.settings import Settings

settings = Settings()

engine_ = create_async_engine(
        url=settings.DB_URL,
)

LocalSession = async_sessionmaker(
        bind=engine_,
        autoflush=False,
        expire_on_commit=False)


@asynccontextmanager
async def create_session() -> AsyncGenerator[AsyncSession, Any]:
     async with LocalSession() as db:
          try:
               yield db
          except Exception as e:
               await db.rollback()
               raise e
