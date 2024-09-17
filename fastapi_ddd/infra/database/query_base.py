from typing import Generic, Optional, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_ddd.domain.entity import Base, EntityId

DomainType = TypeVar("DomainType", bound=Base)


class QueryBase(Generic[DomainType]):
    def __init__(
        self,
        domain: Type[DomainType],
    ):
        self.domain: type[DomainType] = domain

    def find_by_id(self, session: Session, entity_id: EntityId) -> Optional[DomainType]:
        return session.get(self.domain, entity_id.uuid)

    def find_all(self, session: Session, *, skip: int = 0, limit: int = 100) -> list[DomainType]:
        stmt = select(self.domain).offset(skip).limit(limit)

        results: list[DomainType] = session.execute(stmt).scalars().all()

        return results

    def create(self, session: Session, domain: DomainType) -> DomainType:
        session.add(domain)
        session.flush()

    def delete(self, session: Session, entity_id: EntityId) -> None:
        domain: Optional[DomainType] = session.get(self.domain, entity_id.uuid)

        session.delete(domain)
