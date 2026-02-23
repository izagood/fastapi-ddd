from abc import ABC, abstractmethod
from typing import Optional

from fastapi_ddd.domain.entity import EntityId
from fastapi_ddd.domain.member.member import Member


class MemberRepository(ABC):
    @abstractmethod
    async def create(self, member: Member) -> None: ...

    @abstractmethod
    async def find_by_id(self, entity_id: EntityId) -> Member: ...

    @abstractmethod
    async def find_all(self, *, skip: int = 0, limit: int = 100) -> list[Member]: ...

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[Member]: ...

    @abstractmethod
    async def exists_by_email(self, email: str) -> bool: ...
