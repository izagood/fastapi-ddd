from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_ddd.common.exception.custom_exceptions import DatabaseIdNotFoundException
from fastapi_ddd.domain.entity import EntityId
from fastapi_ddd.domain.member.member import Member
from fastapi_ddd.infra.database.query_base import QueryBase


class MemberRepository:
    def __init__(self) -> None:
        self.query_base = QueryBase(Member)

    def create(self, session: Session, member: Member) -> Member:
        return self.query_base.create(session, member)

    def find_by_id(self, session: Session, entity_id: EntityId) -> Member:
        stmt = select(Member).where(Member.id == entity_id.uuid).where(Member.deleted == False)  # noqa: E712

        member: Optional[Member] = session.scalars(stmt).first()

        if member is None:
            raise DatabaseIdNotFoundException()

        return member

    def find_all(self, session: Session, *, skip: int = 0, limit: int = 100) -> list[Member]:
        stmt = select(Member).where(Member.deleted == False)  # noqa: E712

        return session.scalars(stmt).all()
