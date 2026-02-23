import importlib
import inspect
import os
import pkgutil

from loguru import logger

from fastapi_ddd.domain.entity import Base
from fastapi_ddd.infra.database.database import Database

_db: Database | None = None


def get_db() -> Database:
    if _db is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return _db


def find_base_subclasses(package_name: str) -> None:
    logger.info(f"Finding Base subclasses in {package_name}...")

    package = importlib.import_module(package_name)
    package_path = package.__path__

    for _, module_name, is_pkg in pkgutil.iter_modules(package_path):
        full_module_name = f"{package_name}.{module_name}"
        module = importlib.import_module(full_module_name)

        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Base) and obj.__module__ == full_module_name:
                globals()[name] = obj
                logger.info(f"Imported {name} from {full_module_name}")

        if is_pkg:
            find_base_subclasses(full_module_name)


async def init_db() -> None:
    global _db
    logger.info("Database initialization started...")
    find_base_subclasses("fastapi_ddd.domain")
    _db = Database()

    auto_create = os.getenv("AUTO_CREATE_TABLES", "true").lower() == "true"
    if auto_create:
        await _db.create_database()
        logger.info("Tables created via create_all (AUTO_CREATE_TABLES=true).")
    else:
        logger.info("Skipping create_all (AUTO_CREATE_TABLES=false). Use Alembic for migrations.")

    logger.info("Database initialization finished.")


async def close_db() -> None:
    global _db
    if _db is not None:
        logger.info("Closing database connections...")
        await _db.close()
        _db = None
        logger.info("Database connections closed.")
