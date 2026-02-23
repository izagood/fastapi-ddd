from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_ddd.application.member.member_service import MemberService
from fastapi_ddd.infra.database.init_db import get_db
from fastapi_ddd.infra.database.unit_of_work import UnitOfWork


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    session = get_db().session_maker()
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


async def get_uow(session: AsyncSession = Depends(get_async_session)) -> AsyncGenerator[UnitOfWork, None]:
    async with UnitOfWork(session) as uow:
        yield uow


async def get_member_service(uow: UnitOfWork = Depends(get_uow)) -> MemberService:
    return MemberService(uow)
