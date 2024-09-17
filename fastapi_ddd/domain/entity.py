from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


class Base(DeclarativeBase):
    pass


class EntityId:
    def __init__(self, id: UUID) -> None:
        self.uuid = id

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)):
            return self.uuid == other.uuid
        return False

    def __hash__(self) -> int:
        return hash(self.uuid)

    def __str__(self) -> str:
        return str(self.uuid)

    @classmethod
    def create(cls) -> "EntityId":
        return cls(uuid4())

    @classmethod
    def of(cls, id: str) -> "EntityId":
        return cls(UUID(hex=id, version=4))


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())


class BaseWithTime(Base, TimestampMixin):
    __abstract__ = True
