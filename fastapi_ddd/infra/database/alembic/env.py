import asyncio
from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from fastapi_ddd.domain.entity import Base

# Ensure all models are imported so metadata is populated
from fastapi_ddd.domain.member.member import Member  # noqa: F401

config = context.config

# URL이 프로그래밍 방식으로 이미 설정되었으면 (테스트 등) infra_settings import를 건너뜀
if not config.get_main_option("sqlalchemy.url"):
    from fastapi_ddd.common.config.infra_config import infra_settings

    config.set_main_option("sqlalchemy.url", infra_settings.DB.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def _is_sqlite(url: str) -> bool:
    return url.startswith("sqlite")


def _to_sync_url(url: str) -> str:
    """async 드라이버를 동기 드라이버로 변환 (e.g. sqlite+aiosqlite -> sqlite)"""
    return url.replace("+aiosqlite", "").replace("+asyncpg", "")


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_sync_migrations() -> None:
    url = _to_sync_url(config.get_main_option("sqlalchemy.url"))
    connectable = create_engine(url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        do_run_migrations(connection)

    connectable.dispose()


def run_migrations_online() -> None:
    url = config.get_main_option("sqlalchemy.url")
    if _is_sqlite(url):
        run_sync_migrations()
    else:
        asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
