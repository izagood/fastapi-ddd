from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_ddd.common.exception.custom_exceptions import DatabaseIdNotFoundException
from fastapi_ddd.domain.entity import EntityId
from fastapi_ddd.domain.member.member import Member
from fastapi_ddd.infra.database.query_base import QueryBase


class MemberRepository:
    def __init__(self) -> None:
        self.query_base = QueryBase(Member)

    async def create(self, session: AsyncSession, member: Member) -> None:
        await self.query_base.create(session, member)

    async def find_by_id(self, session: AsyncSession, entity_id: EntityId) -> Member:
        stmt = select(Member).where(Member.id == entity_id.uuid).where(Member.deleted == False)  # noqa: E712

        result = await session.execute(stmt)
        member: Optional[Member] = result.scalars().first()

        if member is None:
            raise DatabaseIdNotFoundException()

        return member

    async def find_all(self, session: AsyncSession, *, skip: int = 0, limit: int = 100) -> list[Member]:
        stmt = select(Member).where(Member.deleted == False).offset(skip).limit(limit)  # noqa: E712

        result = await session.execute(stmt)
        return list(result.scalars().all())
