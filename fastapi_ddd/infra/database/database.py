from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from fastapi_ddd.common.config.infra_config import infra_settings
from fastapi_ddd.domain.entity import Base

SQLALCHEMY_DATABASE_URL = infra_settings.DB.URL


class Database:
    def __init__(self, database_url: str = SQLALCHEMY_DATABASE_URL) -> None:
        self._engine = create_async_engine(database_url, echo=True, pool_pre_ping=True)
        self._session_maker = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

    async def create_database(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def close(self) -> None:
        await self._engine.dispose()

    @property
    def session_maker(self) -> async_sessionmaker[AsyncSession]:
        return self._session_maker
