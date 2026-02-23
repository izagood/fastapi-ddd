from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_ddd.domain.entity import EntityId
from fastapi_ddd.domain.exceptions import DuplicateEmailException, MemberNotFoundException
from fastapi_ddd.domain.member.member import Member
from fastapi_ddd.domain.member.member_repository import MemberRepository


class SqlAlchemyMemberRepository(MemberRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, member: Member) -> None:
        self._session.add(member)
        try:
            await self._session.flush()
        except IntegrityError as e:
            await self._session.rollback()
            if "email" in str(e.orig).lower():
                raise DuplicateEmailException(member.email) from e
            raise

    async def find_by_id(self, entity_id: EntityId) -> Member:
        stmt = select(Member).where(Member.id == entity_id.uuid).where(Member.deleted == False)  # noqa: E712
        result = await self._session.execute(stmt)
        member: Optional[Member] = result.scalars().first()

        if member is None:
            raise MemberNotFoundException()

        return member

    async def find_all(self, *, skip: int = 0, limit: int = 100) -> list[Member]:
        stmt = select(Member).where(Member.deleted == False).offset(skip).limit(limit)  # noqa: E712
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def find_by_email(self, email: str) -> Optional[Member]:
        stmt = select(Member).where(Member.email == email).where(Member.deleted == False)  # noqa: E712
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def exists_by_email(self, email: str) -> bool:
        member = await self.find_by_email(email)
        return member is not None
