from pydantic_settings import BaseSettings


class FastAPISettings(BaseSettings):
    TITLE: str = "FastAPI DDD"
    VERSION: str = "0.1.0"


class Settings(BaseSettings):
    FAST_API: FastAPISettings = FastAPISettings()


app_settings = Settings()
