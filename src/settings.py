import enum
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

    # Logger Provider for message outputs system, it can configure
    # using different types of provider,
    # it depends on adapters that you have, this applies la configuration of that logger
    logger_provider: str
    env_provider: str
    http_provider: str
    server_provider: str

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


class ProdSettings(BaseSettings):
    environment = EnvironmentType.prod

    logger_provider = "logging"
    env_provider = "dotenv-python"
    http_provider = "fastapi"
    server_provider = "uvicorn"
