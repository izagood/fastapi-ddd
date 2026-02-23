import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from fastapi_ddd.domain.entity import Base
from fastapi_ddd.infra.database.member_repository_impl import SqlAlchemyMemberRepository
from fastapi_ddd.infra.database.unit_of_work import UnitOfWork

from tests.integration.alembic_utils import run_downgrade, run_upgrade


@pytest.fixture(scope="session")
def db_url(tmp_path_factory):
    db_path = tmp_path_factory.mktemp("data") / "test.db"
    return f"sqlite+aiosqlite:///{db_path}"


@pytest.fixture(scope="session", autouse=True)
def apply_migrations(db_url):
    run_upgrade(db_url)
    yield
    run_downgrade(db_url)


@pytest.fixture(scope="session")
def engine(db_url):
    return create_async_engine(db_url, echo=True)


@pytest.fixture(autouse=True)
async def clean_tables(engine):
    yield
    async with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())


@pytest.fixture
async def session(engine):
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as session:
        yield session
        await session.rollback()


@pytest.fixture
def repository(session):
    return SqlAlchemyMemberRepository(session)


@pytest.fixture
def uow(session):
    return UnitOfWork(session)
