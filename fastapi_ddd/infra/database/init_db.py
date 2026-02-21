import importlib
import inspect
import pkgutil

from loguru import logger

from fastapi_ddd.domain.entity import Base
from fastapi_ddd.infra.database.database import Database

db = Database()


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
    logger.info("Database initialization started...")
    find_base_subclasses("fastapi_ddd.domain")
    await db.create_database()
    logger.info("Database initialization finished.")


async def close_db() -> None:
    logger.info("Closing database connections...")
    await db.close()
    logger.info("Database connections closed.")
