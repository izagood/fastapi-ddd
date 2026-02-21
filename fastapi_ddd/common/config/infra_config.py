import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

project_root = Path(__file__).resolve().parent.parent.parent
load_dotenv(project_root)


class Database(BaseSettings):
    DBMS: str
    DRIVER: str
    USER: str
    PWD: str
    HOST: str
    PORT: str
    NAME: str
    URL: str


class DatabaseFactory:
    @staticmethod
    def create() -> Database:
        dbms = "postgresql"
        driver = "asyncpg"

        name: str = os.getenv("DB_NAME", "fastapi_ddd")
        user: str = os.getenv("DB_USER", "postgres")
        pwd: str = os.getenv("DB_PASSWORD", "postgres")

        host: str = os.getenv("BE_DB_HOST", "localhost")
        port: str = os.getenv("BE_DB_PORT", "5432")

        url: str = f"{dbms}+{driver}://{user}:{pwd}@{host}:{port}/{name}"

        return Database(
            DBMS=dbms,
            DRIVER=driver,
            USER=user,
            PWD=pwd,
            HOST=host,
            PORT=port,
            NAME=name,
            URL=url,
        )


class Settings(BaseSettings):
    DB: Database = DatabaseFactory.create()


infra_settings = Settings()
