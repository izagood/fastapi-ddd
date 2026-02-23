import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from fastapi_ddd.main import app
from fastapi_ddd.infra.dependencies import get_async_session

from tests.integration.alembic_utils import run_downgrade, run_upgrade

VALID_PASSWORD = "Test@1234"


@pytest.fixture
def api_db_url(tmp_path):
    db_path = tmp_path / "api_test.db"
    return f"sqlite+aiosqlite:///{db_path}"


@pytest.fixture
def api_engine(api_db_url):
    run_upgrade(api_db_url)
    engine = create_async_engine(api_db_url, echo=True)
    yield engine
    run_downgrade(api_db_url)


@pytest.fixture
async def api_client(api_engine):
    session_factory = async_sessionmaker(api_engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_session():
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_async_session] = override_get_session
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


async def _create_member(client, email="test@example.com", name="Test User"):
    response = await client.post(
        "/api/v1/members/",
        json={"email": email, "passwd": VALID_PASSWORD, "name": name},
    )
    return response


class TestMemberAPI:
    async def test_create_member_endpoint(self, api_client):
        response = await _create_member(api_client, "new@example.com", "New User")
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "new@example.com"
        assert data["name"] == "New User"
        assert "id" in data

    async def test_get_member_endpoint(self, api_client):
        create_resp = await _create_member(api_client, "get@example.com", "Get User")
        member_id = create_resp.json()["id"]

        response = await api_client.get(f"/api/v1/members/{member_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "get@example.com"
        assert data["id"] == member_id

    async def test_get_member_not_found(self, api_client):
        response = await api_client.get("/api/v1/members/00000000-0000-4000-8000-000000000000")
        assert response.status_code == 404

    async def test_get_all_members_endpoint(self, api_client):
        await _create_member(api_client, "a@example.com", "A")
        await _create_member(api_client, "b@example.com", "B")

        response = await api_client.get("/api/v1/members/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    async def test_create_member_duplicate_email(self, api_client):
        await _create_member(api_client, "dup@example.com", "First")
        response = await _create_member(api_client, "dup@example.com", "Second")
        assert response.status_code == 409

    async def test_create_member_invalid_email(self, api_client):
        response = await api_client.post(
            "/api/v1/members/",
            json={"email": "bad-email", "passwd": VALID_PASSWORD, "name": "Test"},
        )
        assert response.status_code == 422

    async def test_update_member_profile(self, api_client):
        create_resp = await _create_member(api_client, "patch@example.com", "Old")
        member_id = create_resp.json()["id"]

        response = await api_client.patch(
            f"/api/v1/members/{member_id}",
            json={"name": "New Name"},
        )
        assert response.status_code == 200
        assert response.json()["name"] == "New Name"

    async def test_change_password(self, api_client):
        create_resp = await _create_member(api_client, "pw@example.com", "PW User")
        member_id = create_resp.json()["id"]

        response = await api_client.patch(
            f"/api/v1/members/{member_id}/password",
            json={"passwd": "NewPass@123"},
        )
        assert response.status_code == 200

    async def test_change_email(self, api_client):
        create_resp = await _create_member(api_client, "old@example.com", "Email User")
        member_id = create_resp.json()["id"]

        response = await api_client.patch(
            f"/api/v1/members/{member_id}/email",
            json={"email": "new@example.com"},
        )
        assert response.status_code == 200
        assert response.json()["email"] == "new@example.com"

    async def test_change_email_duplicate(self, api_client):
        await _create_member(api_client, "existing@example.com", "Existing")
        create_resp = await _create_member(api_client, "change@example.com", "Changer")
        member_id = create_resp.json()["id"]

        response = await api_client.patch(
            f"/api/v1/members/{member_id}/email",
            json={"email": "existing@example.com"},
        )
        assert response.status_code == 409

    async def test_delete_member(self, api_client):
        create_resp = await _create_member(api_client, "del@example.com", "Del User")
        member_id = create_resp.json()["id"]

        response = await api_client.delete(f"/api/v1/members/{member_id}")
        assert response.status_code == 204

        get_resp = await api_client.get(f"/api/v1/members/{member_id}")
        assert get_resp.status_code == 404

    async def test_invalid_uuid_returns_400(self, api_client):
        response = await api_client.get("/api/v1/members/not-a-uuid")
        assert response.status_code == 400

    async def test_health_check(self, api_client):
        response = await api_client.get("/api/v1/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
