from fastapi_ddd.common.config.app_config import CORSSettings


class TestCORSSettings:
    def test_wildcard_origins(self):
        settings = CORSSettings(CORS_ORIGINS="*")
        assert settings.origins_list == ["*"]

    def test_custom_origins(self):
        settings = CORSSettings(CORS_ORIGINS="http://localhost:3000, http://example.com")
        assert settings.origins_list == ["http://localhost:3000", "http://example.com"]

    def test_wildcard_methods(self):
        settings = CORSSettings(CORS_ALLOW_METHODS="*")
        assert settings.methods_list == ["*"]

    def test_custom_methods(self):
        settings = CORSSettings(CORS_ALLOW_METHODS="GET, POST")
        assert settings.methods_list == ["GET", "POST"]

    def test_wildcard_headers(self):
        settings = CORSSettings(CORS_ALLOW_HEADERS="*")
        assert settings.headers_list == ["*"]

    def test_custom_headers(self):
        settings = CORSSettings(CORS_ALLOW_HEADERS="Authorization, Content-Type")
        assert settings.headers_list == ["Authorization", "Content-Type"]
