from unittest.mock import AsyncMock

import pytest

from fastapi_ddd.domain.exceptions import DuplicateEmailException
from fastapi_ddd.domain.member.member_domain_service import MemberDomainService
from fastapi_ddd.domain.member.value_objects import Email


class TestMemberDomainService:
    async def test_ensure_email_unique_passes(self):
        repo = AsyncMock()
        repo.exists_by_email = AsyncMock(return_value=False)
        service = MemberDomainService(repo)

        await service.ensure_email_unique(Email("new@example.com"))
        repo.exists_by_email.assert_awaited_once_with("new@example.com")

    async def test_ensure_email_unique_raises_on_duplicate(self):
        repo = AsyncMock()
        repo.exists_by_email = AsyncMock(return_value=True)
        service = MemberDomainService(repo)

        with pytest.raises(DuplicateEmailException, match="dup@example.com"):
            await service.ensure_email_unique(Email("dup@example.com"))
