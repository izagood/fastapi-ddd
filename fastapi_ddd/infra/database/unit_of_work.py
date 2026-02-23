from types import TracebackType
from typing import Optional, Self

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_ddd.domain.member.member_repository import MemberRepository
from fastapi_ddd.infra.database.member_repository_impl import SqlAlchemyMemberRepository


class UnitOfWork:
    members: MemberRepository

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self.members = SqlAlchemyMemberRepository(session)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if exc_type is not None:
            await self.rollback()

    async def commit(self) -> None:
        await self._session.commit()

    async def refresh(self, instance: object) -> None:
        await self._session.refresh(instance)

    async def rollback(self) -> None:
        await self._session.rollback()
