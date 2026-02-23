from typing import Protocol, runtime_checkable

from fastapi_ddd.domain.member.member_repository import MemberRepository


@runtime_checkable
class AbstractUnitOfWork(Protocol):
    members: MemberRepository

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...

    async def refresh(self, instance: object) -> None: ...
