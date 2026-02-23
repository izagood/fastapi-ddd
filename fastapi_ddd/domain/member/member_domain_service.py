from fastapi_ddd.domain.exceptions import DuplicateEmailException
from fastapi_ddd.domain.member.member_repository import MemberRepository
from fastapi_ddd.domain.member.value_objects import Email


class MemberDomainService:
    def __init__(self, member_repository: MemberRepository) -> None:
        self._repository = member_repository

    async def ensure_email_unique(self, email: Email) -> None:
        if await self._repository.exists_by_email(email.value):
            raise DuplicateEmailException(email.value)
