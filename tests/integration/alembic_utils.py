from pathlib import Path

from alembic import command
from alembic.config import Config

_PROJECT_ROOT = Path(__file__).resolve().parents[2]


def get_alembic_config(database_url: str) -> Config:
    """테스트용 Alembic Config를 생성하고 URL을 오버라이드한다."""
    ini_path = _PROJECT_ROOT / "alembic.ini"
    cfg = Config(str(ini_path))
    # async 드라이버를 동기로 변환 (env.py에서 처리하지만 URL 자체도 설정)
    cfg.set_main_option("sqlalchemy.url", database_url)
    return cfg


def run_upgrade(database_url: str, revision: str = "head") -> None:
    cfg = get_alembic_config(database_url)
    command.upgrade(cfg, revision)


def run_downgrade(database_url: str, revision: str = "base") -> None:
    cfg = get_alembic_config(database_url)
    command.downgrade(cfg, revision)
