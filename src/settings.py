import datetime
import enum
import pathlib
from typing import Any, Dict

# Types


class EnvironmentType(enum.StrEnum):
    prod = enum.auto()
    dev = enum.auto()


# Base


class BaseSettings:
    title: str = "DDD-Abs-Lib-Standard"
    summary: str = (
        "A App for generate with DDD and abstract libraries configuration for extend all"
    )
    contact_info: Dict[str, str] = {
        "name": "Gabriel Vargas Monroy",
        "url": "https://vmgabriel.com",
        "email": "vmgabriel96@gmail.com",
    }

    debug_level: str = "INFO"

    environment: EnvironmentType = EnvironmentType.prod

    # Server
    host: str = "0.0.0.0"
    port: int = 3030

    # Documentation URL for api if this is required
    docs_url: str = "/docs"
    prefix_api_url: str = "/api"

    # Security and Auth
    auth_type: str = "Bearer"
    authorization_name_attribute: str = "Authorization"
    expiration_access_token: datetime.timedelta = datetime.timedelta(hours=2)
    expiration_refresh_token: datetime.timedelta = datetime.timedelta(days=2)
    auth_access_token_secret: str = ""
    auth_refresh_token_secret: str = ""

    # Logger Provider for message outputs system, it can configure
    # using different types of provider,
    # it depends on adapters that you have, this applies la configuration of that logger
    logger_provider: str
    env_provider: str
    http_provider: str
    server_provider: str
    jwt_provider: str
    uow_provider: str
    migrator_provider: str
    repository_provider: str
    cli_provider: str

    # Postgres Data
    postgres_port: str = "5432"
    postgres_dbname: str = ""
    postgres_host: str = ""
    postgres_username: str = ""
    postgres_password: str = ""

    app_route: pathlib.Path = pathlib.Path(__file__).parent

    @property
    def has_debug(self) -> bool:
        return self.debug_level != "NONE"

    def inject(self, data: Dict[str, Any]):
        for key, value in data.items():
            setattr(self, key, value)


# Hierarchies


class DevSettings(BaseSettings):
    environment = EnvironmentType.dev

    logger_provider = "logging"
    env_provider = "dotenv-python"
    http_provider = "fastapi"
    server_provider = "uvicorn"
    jwt_provider = "pyjwt"
    uow_provider = "psycopg"
    migrator_provider = "psycopg"
    repository_provider = "psycopg"
    cli_provider = "cyclopts"

    postgres_dbname = "postgres"
    postgres_host = "db"
    postgres_username = "ghost"
    postgres_password = "rider"


class ProdSettings(BaseSettings):
    environment = EnvironmentType.prod

    logger_provider = "logging"
    env_provider = "dotenv-python"
    http_provider = "fastapi"
    server_provider = "uvicorn"
    jwt_provider = "pyjwt"
    uow_provider = "psycopg"
    migrator_provider = "psycopg"
    repository_provider = "psycopg"
    cli_provider = "cyclopts"

    postgres_dbname = "."
    postgres_host = "."
    postgres_username = "."
    postgres_password = "."
