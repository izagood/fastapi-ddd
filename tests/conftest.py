from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest

from fastapi_ddd.domain.member.member import Member
from fastapi_ddd.infra.database.unit_of_work import UnitOfWork

VALID_PASSWORD = "Test@1234"


@pytest.fixture
def mock_session():
    session = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.close = AsyncMock()
    session.flush = AsyncMock()
    session.add = AsyncMock()
    session.execute = AsyncMock()
    session.get = AsyncMock()
    return session


@pytest.fixture
def mock_uow(mock_session):
    return UnitOfWork(mock_session)


@pytest.fixture
def sample_member():
    now = datetime.now(timezone.utc)
    member = Member(email="test@example.com", passwd=VALID_PASSWORD, name="Test User")
    member.created_at = now
    member.updated_at = now
    return member
