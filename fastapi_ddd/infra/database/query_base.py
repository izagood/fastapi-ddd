from typing import Generic, Optional, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_ddd.domain.entity import Base, EntityId

DomainType = TypeVar("DomainType", bound=Base)


class QueryBase(Generic[DomainType]):
    def __init__(
        self,
        domain: Type[DomainType],
    ):
        self.domain: type[DomainType] = domain

    async def find_by_id(self, session: AsyncSession, entity_id: EntityId) -> Optional[DomainType]:
        return await session.get(self.domain, entity_id.uuid)

    async def find_all(self, session: AsyncSession, *, skip: int = 0, limit: int = 100) -> list[DomainType]:
        stmt = select(self.domain).offset(skip).limit(limit)

        result = await session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, session: AsyncSession, domain: DomainType) -> None:
        session.add(domain)
        await session.flush()

    async def delete(self, session: AsyncSession, entity_id: EntityId) -> None:
        domain: Optional[DomainType] = await session.get(self.domain, entity_id.uuid)

        await session.delete(domain)
