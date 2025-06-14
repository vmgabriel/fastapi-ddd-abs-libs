import enum
from typing import Any, Dict

# Types


class EnvironmentType(enum.StrEnum):
    prod = enum.auto()
    dev = enum.auto()


# Base


class BaseSettings:
    title: str = "DDD-Abs-Lib-Standard"
    debug_level: str = "INFO"

    environment: EnvironmentType = EnvironmentType.prod

    # Logger Provider for message outputs system, it can configure
    # using different types of provider,
    # it depends on adapters that you have, this applies la configuration of that logger
    logger_provider: str
    env_provider: str

    def inject(self, data: Dict[str, Any]):
        for key, value in data.items():
            setattr(self, key, value)


# Hierarchies


class DevSettings(BaseSettings):
    environment = EnvironmentType.dev

    logger_provider = "logging"
    env_provider = "dotenv-python"


class ProdSettings(BaseSettings):
    environment = EnvironmentType.prod

    logger_provider = "logging"
    env_provider = "dotenv-python"
