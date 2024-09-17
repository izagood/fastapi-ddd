import importlib
import inspect
import os
import pkgutil

from fastapi_ddd.domain.entity import Base
from fastapi_ddd.infra.database.database import Database


def find_base_subclasses(package_name):
    print(f"Finding Base subclasses in {package_name}...")

    package = importlib.import_module(package_name)
    package_path = package.__path__

    for _, module_name, is_pkg in pkgutil.iter_modules(package_path):
        full_module_name = f"{package_name}.{module_name}"
        module = importlib.import_module(full_module_name)

        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Base) and obj.__module__ == full_module_name:
                globals()[name] = obj
                print(f"Imported {name} from {full_module_name}")

        if is_pkg:
            find_base_subclasses(full_module_name)


def create_database_tables():
    print("Database tables creation started...")

    dbms = "postgresql"
    driver = "psycopg2"

    name: str = os.getenv("DB_NAME")
    user: str = os.getenv("DB_USER")
    pwd: str = os.getenv("DB_PASSWORD")

    host: str = "localhost"
    port: str = os.getenv("DB_PORT")

    url: str = f"{dbms}+{driver}://{user}:{pwd}@{host}:{port}/{name}"

    db = Database(url)
    db.create_database()

    print("Database tables creation finished.")


ENVIRON_SET: str = os.getenv("ENVIRON_SET").lower()
print(f"ENVIRON_SET: {ENVIRON_SET}")

if ENVIRON_SET == "ci" or ENVIRON_SET == "dev":
    package_name = "fastapi_ddd.domain"
    find_base_subclasses(package_name)

    create_database_tables()
