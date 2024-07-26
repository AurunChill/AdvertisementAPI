from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


PROJECT_PATH = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_PATH / ".env"

if not ENV_PATH.exists():
    raise FileNotFoundError(f"Environment file not found at {ENV_PATH}")

load_dotenv(dotenv_path=ENV_PATH, verbose=True)


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(ENV_PATH), env_file_encoding="utf-8", extra="allow")


class AdminSettings(EnvSettings):
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    ADMIN_SECRET_SESSION: str


class DatabaseSettings(EnvSettings):
    DB_USER: str
    DB_PORT: str
    DB_PASS: str
    DB_HOST: str
    DB_NAME: str

    @property
    def DATABASE_URL_ASYNC(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def DATABASE_URL(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class TestDatabaseSettings(EnvSettings):
    DB_TEST_USER: str
    DB_TEST_PORT: str
    DB_TEST_PASS: str
    DB_TEST_HOST: str
    DB_TEST_NAME: str

    @property
    def DATABASE_URL_ASYNC(self):
        return f"postgresql+asyncpg://{self.DB_TEST_USER}:{self.DB_TEST_PASS}@{self.DB_TEST_HOST}:{self.DB_TEST_PORT}/{self.DB_TEST_NAME}"
    
    @property
    def DATABASE_URL(self):
        return f"postgresql+psycopg2://{self.DB_TEST_USER}:{self.DB_TEST_PASS}@{self.DB_TEST_HOST}:{self.DB_TEST_PORT}/{self.DB_TEST_NAME}"


class TestSettings(EnvSettings):
    IS_TESTING: bool
    BASE_URL: str


class LoggingSettings:
    LOG_PATH = PROJECT_PATH / "logs"


class MiddlewareSettings:
    BACKEND_CORS_ORIGINS: list[str] = []


class APISettings(EnvSettings):
    API_VERSION: int


class AuthSettings(EnvSettings):
    SECRET_MANAGER: str
    SECRET_JWT: str


class Settings():
    api = APISettings()
    auth = AuthSettings()
    admin = AdminSettings()
    database = DatabaseSettings()
    middleware = MiddlewareSettings()
    test_database = TestDatabaseSettings()
    test = TestSettings()
    log = LoggingSettings()


settings = Settings()