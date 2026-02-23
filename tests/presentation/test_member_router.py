from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import ASGITransport, AsyncClient

from fastapi_ddd.domain.member.member import Member
from fastapi_ddd.main import app
from fastapi_ddd.infra.dependencies import get_async_session

VALID_PASSWORD = "Test@1234"


def _make_mock_session(*, find_result=None, find_all_result=None):
    session = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.close = AsyncMock()
    session.flush = AsyncMock()
    session.add = MagicMock()
    session.get = AsyncMock()

    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.first.return_value = find_result
    mock_scalars.all.return_value = find_all_result or []
    mock_result.scalars.return_value = mock_scalars
    session.execute = AsyncMock(return_value=mock_result)

    return session


@pytest.fixture
def mock_session():
    return _make_mock_session()


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
                "/api/v1/members/",
                json={"email": "new@example.com", "passwd": VALID_PASSWORD, "name": "New User"},
            )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "new@example.com"
        assert data["name"] == "New User"

    async def test_create_member_invalid_email(self, client):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post(
                "/api/v1/members/",
                json={"email": "not-email", "passwd": VALID_PASSWORD, "name": "Test"},
            )

        assert response.status_code == 422

    async def test_create_member_weak_password(self, client):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post(
                "/api/v1/members/",
                json={"email": "test@example.com", "passwd": "weak", "name": "Test"},
            )

        assert response.status_code == 422


class TestGetMembersEndpoint:
    async def test_get_members(self):
        member = Member(email="a@example.com", passwd=VALID_PASSWORD, name="A")
        session = _make_mock_session(find_all_result=[member])

        async def override():
            yield session

        app.dependency_overrides[get_async_session] = override
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/api/v1/members/")
        app.dependency_overrides.clear()

        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestGetMemberEndpoint:
    async def test_get_member_not_found(self, client):
        transport = ASGITransport(app=app, raise_app_exceptions=False)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/api/v1/members/00000000-0000-4000-8000-000000000000")

        assert response.status_code == 404


class TestUpdateMemberEndpoint:
    async def test_update_member_profile(self):
        member = Member(email="u@example.com", passwd=VALID_PASSWORD, name="Old")
        session = _make_mock_session(find_result=member)

        async def override():
            yield session

        app.dependency_overrides[get_async_session] = override
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.patch(
                f"/api/v1/members/{member.id}",
                json={"name": "New"},
            )
        app.dependency_overrides.clear()

        assert response.status_code == 200
        assert response.json()["name"] == "New"


class TestChangePasswordEndpoint:
    async def test_change_password(self):
        member = Member(email="pw@example.com", passwd=VALID_PASSWORD, name="PW")
        session = _make_mock_session(find_result=member)

        async def override():
            yield session

        app.dependency_overrides[get_async_session] = override
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.patch(
                f"/api/v1/members/{member.id}/password",
                json={"passwd": "NewPass@123"},
            )
        app.dependency_overrides.clear()

        assert response.status_code == 200


class TestDeleteMemberEndpoint:
    async def test_delete_member(self):
        member = Member(email="del@example.com", passwd=VALID_PASSWORD, name="Del")
        session = _make_mock_session(find_result=member)

        async def override():
            yield session

        app.dependency_overrides[get_async_session] = override
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.delete(f"/api/v1/members/{member.id}")
        app.dependency_overrides.clear()

        assert response.status_code == 204
