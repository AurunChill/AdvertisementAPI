from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


# Define the project path and path for the environment variables file.
PROJECT_PATH = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_PATH / ".env"

# Load environment variables from the .env file and raise an error if it does not exist.
if not ENV_PATH.exists():
    raise FileNotFoundError(f"Environment file not found at {ENV_PATH}")

load_dotenv(dotenv_path=ENV_PATH, verbose=True)


class EnvSettings(BaseSettings):
    """
    Base settings class that loads environment variables into Pydantic settings.
    
    This class provides a configuration dictionary for loading environment 
    variables from the specified .env file with UTF-8 encoding and allows 
    for extra fields.
    """
    model_config = SettingsConfigDict(env_file=str(ENV_PATH), env_file_encoding="utf-8", extra="allow")


class AdminSettings(EnvSettings):
    """Settings for the admin user including credentials and session secret."""
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    ADMIN_SECRET_SESSION: str


class DatabaseSettings(EnvSettings):
    """Database connection settings for the application."""
    DB_USER: str
    DB_PORT: str
    DB_PASS: str
    DB_HOST: str
    DB_NAME: str

    @property
    def DATABASE_URL_ASYNC(self):
        """Builds the asynchronous database connection URL."""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def DATABASE_URL(self):
        """Builds the synchronous database connection URL."""
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class TestDatabaseSettings(EnvSettings):
    """Database settings specifically for testing purposes."""
    DB_TEST_USER: str
    DB_TEST_PORT: str
    DB_TEST_PASS: str
    DB_TEST_HOST: str
    DB_TEST_NAME: str

    @property
    def DATABASE_URL_ASYNC(self):
        """Builds the asynchronous test database connection URL."""
        return f"postgresql+asyncpg://{self.DB_TEST_USER}:{self.DB_TEST_PASS}@{self.DB_TEST_HOST}:{self.DB_TEST_PORT}/{self.DB_TEST_NAME}"
    
    @property
    def DATABASE_URL(self):
        """Builds the synchronous test database connection URL."""
        return f"postgresql+psycopg2://{self.DB_TEST_USER}:{self.DB_TEST_PASS}@{self.DB_TEST_HOST}:{self.DB_TEST_PORT}/{self.DB_TEST_NAME}"


class TestSettings(EnvSettings):
    """Settings for running tests, including a testing flag and base URL."""
    IS_TESTING: bool
    BASE_URL: str


class MailSettings(EnvSettings):
    """Mail server settings for sending emails."""
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: str
    MAIL_SERVER: str
    MAIL_TLS: str
    MAIL_SSL: str


class CelerySettings(EnvSettings):
    """Settings for configuring the Celery task queue."""
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str


class LoggingSettings:
    """Settings related to logging, including the log file path."""
    LOG_PATH = PROJECT_PATH / "logs"


class MiddlewareSettings:
    """Settings for configuring CORS and other middleware-related configurations."""
    BACKEND_CORS_ORIGINS: list[str] = []


class APISettings(EnvSettings):
    """Settings related to API configuration, including the API version."""
    API_VERSION: int


class FixturesSettings:
    """Settings for loading fixture data from files."""
    FIXTURES_PATH = PROJECT_PATH / "src" / "fixtures"


class AuthSettings(EnvSettings):
    """Settings for authentication, including JWT secret and expiration time."""
    SECRET_MANAGER: str
    SECRET_JWT: str
    VERIFY_TOKEN_EXPIRATION: int
    VERIFY_REDIRECT: str = "http://localhost:8080/docs"


class Settings():
    """Container class to group all application settings."""
    api = APISettings()
    auth = AuthSettings()
    admin = AdminSettings()
    database = DatabaseSettings()
    middleware = MiddlewareSettings()
    fixtures = FixturesSettings()
    mail = MailSettings()
    celery = CelerySettings()
    test_database = TestDatabaseSettings()
    test = TestSettings()
    log = LoggingSettings()


settings = Settings()  # Instantiate the settings class to access all configurations.