from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    model_config = {"env_file": ".env", "extra": "ignore"}

    DATABASE_URL: str = "sqlite+aiosqlite:///fastapi_ddd.db"


class Settings(BaseSettings):
    DB: DatabaseSettings = DatabaseSettings()


infra_settings = Settings()
