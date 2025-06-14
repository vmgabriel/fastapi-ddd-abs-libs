import enum

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


# Hierarchies


class DevSettings(BaseSettings):
    environment = EnvironmentType.dev

    logger_provider = "logging"


class ProdSettings(BaseSettings):
    environment = EnvironmentType.prod

    logger_provider = "logging"
