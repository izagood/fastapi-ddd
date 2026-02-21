from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from fastapi_ddd.main import app
from fastapi_ddd.presentation.rest.member_router import get_async_session

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
def client(mock_session):
    async def override_get_session():
        yield mock_session

    app.dependency_overrides[get_async_session] = override_get_session
    yield
    app.dependency_overrides.clear()


class TestCreateMemberEndpoint:
    async def test_create_member(self, client, mock_session):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post(
                "/members/",
                json={"email": "new@example.com", "passwd": VALID_PASSWORD, "name": "New User"},
            )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "new@example.com"
        assert data["name"] == "New User"

    async def test_create_member_invalid_email(self, client):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post(
                "/members/",
                json={"email": "not-email", "passwd": VALID_PASSWORD, "name": "Test"},
            )

        assert response.status_code == 422

    async def test_create_member_weak_password(self, client):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post(
                "/members/",
                json={"email": "test@example.com", "passwd": "weak", "name": "Test"},
            )

        assert response.status_code == 422
