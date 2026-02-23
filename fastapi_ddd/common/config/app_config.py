from pydantic_settings import BaseSettings


class FastAPISettings(BaseSettings):
    TITLE: str = "FastAPI DDD"
    VERSION: str = "0.1.0"


class CORSSettings(BaseSettings):
    model_config = {"env_file": ".env", "extra": "ignore"}

    CORS_ORIGINS: str = "*"
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: str = "*"
    CORS_ALLOW_HEADERS: str = "*"

    @property
    def origins_list(self) -> list[str]:
        if self.CORS_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    @property
    def methods_list(self) -> list[str]:
        if self.CORS_ALLOW_METHODS == "*":
            return ["*"]
        return [method.strip() for method in self.CORS_ALLOW_METHODS.split(",")]

    @property
    def headers_list(self) -> list[str]:
        if self.CORS_ALLOW_HEADERS == "*":
            return ["*"]
        return [header.strip() for header in self.CORS_ALLOW_HEADERS.split(",")]


class Settings(BaseSettings):
    FAST_API: FastAPISettings = FastAPISettings()
    CORS: CORSSettings = CORSSettings()


app_settings = Settings()
