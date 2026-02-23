from sqlalchemy import create_engine, inspect, text

from tests.integration.alembic_utils import run_downgrade, run_upgrade


def _sync_url(async_url: str) -> str:
    return async_url.replace("+aiosqlite", "")


class TestAlembicMigrations:
    def test_upgrade_to_head(self, tmp_path):
        db_path = tmp_path / "mig.db"
        url = f"sqlite+aiosqlite:///{db_path}"

        run_upgrade(url)

        engine = create_engine(_sync_url(url))
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        assert "member" in tables
        engine.dispose()

    def test_downgrade_to_base(self, tmp_path):
        db_path = tmp_path / "mig.db"
        url = f"sqlite+aiosqlite:///{db_path}"

        run_upgrade(url)
        run_downgrade(url)

        engine = create_engine(_sync_url(url))
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        assert "member" not in tables
        engine.dispose()

    def test_upgrade_downgrade_cycle(self, tmp_path):
        db_path = tmp_path / "mig.db"
        url = f"sqlite+aiosqlite:///{db_path}"

        # 1차 upgrade → downgrade
        run_upgrade(url)
        run_downgrade(url)

        # 2차 upgrade → 데이터 삽입 성공 확인
        run_upgrade(url)

        engine = create_engine(_sync_url(url))
        with engine.begin() as conn:
            conn.execute(
                text(
                    "INSERT INTO member (mem_id, email, passwd, name, deleted, created_at, updated_at) "
                    "VALUES (:id, :email, :passwd, :name, :deleted, :created_at, :updated_at)"
                ),
                {
                    "id": "00000000-0000-4000-8000-000000000001",
                    "email": "test@example.com",
                    "passwd": "hashed",
                    "name": "Test",
                    "deleted": False,
                    "created_at": "2026-01-01T00:00:00",
                    "updated_at": "2026-01-01T00:00:00",
                },
            )
            result = conn.execute(text("SELECT count(*) FROM member"))
            assert result.scalar() == 1
        engine.dispose()
