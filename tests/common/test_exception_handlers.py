from unittest.mock import AsyncMock

from fastapi_ddd.common.exception.exception_handlers import (
    domain_entity_not_found_handler,
    domain_exception_handler,
    duplicate_email_handler,
)
from fastapi_ddd.domain.exceptions import DomainException, DuplicateEmailException, EntityNotFoundException


class TestExceptionHandlers:
    async def test_entity_not_found_returns_404(self):
        request = AsyncMock()
        exc = EntityNotFoundException("Member not found")
        response = await domain_entity_not_found_handler(request, exc)
        assert response.status_code == 404

    async def test_duplicate_email_returns_409(self):
        request = AsyncMock()
        exc = DuplicateEmailException("test@example.com")
        response = await duplicate_email_handler(request, exc)
        assert response.status_code == 409

    async def test_domain_exception_returns_400(self):
        request = AsyncMock()
        exc = DomainException("Some rule violated")
        response = await domain_exception_handler(request, exc)
        assert response.status_code == 400
