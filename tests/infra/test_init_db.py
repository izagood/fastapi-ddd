import pytest

from fastapi_ddd.infra.database import init_db as init_db_module


class TestGetDb:
    def test_get_db_raises_when_not_initialized(self):
        original = init_db_module._db
        try:
            init_db_module._db = None
            with pytest.raises(RuntimeError, match="Database not initialized"):
                init_db_module.get_db()
        finally:
            init_db_module._db = original
