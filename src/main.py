from logging import getLogger
from typing import Any, Dict

from src import settings
from src.fastapi_ddd_abs_libs import base as base_infra
from src.infra.environment_variable import request as request_environment_variable
from src.infra.http import model as model_http
from src.infra.http import request as request_http
from src.infra.log import request as request_logger

log = getLogger(__name__)


def build() -> model_http.AppHttp:
    dependencies: Dict[str, Any] = {}
    configuration = build_configuration()

    dependencies["configuration"] = configuration

    logger_builder = build_logger_adapter(configuration)
    env_builder = build_env_adapter(configuration)

    env_adapter = env_builder.selected_with_configuration(dependencies=dependencies)
    configuration.inject(env_adapter.all())

    dependencies["logger"] = logger_builder.selected_with_configuration(
        dependencies=dependencies
    )
    dependencies["env"] = env_adapter
    dependencies["http"] = build_http_adapter(
        configuration
    ).selected_with_configuration(dependencies=dependencies)

    return dependencies["http"].execute()


def build_configuration() -> settings.BaseSettings:
    return settings.DevSettings()


def build_logger_adapter(configuration: settings.BaseSettings) -> base_infra.InfraBase:
    return base_infra.InfraBase(
        request=request_logger,
        logger_adapter=log,
        configurations=configuration,
    )


def build_env_adapter(configuration: settings.BaseSettings) -> base_infra.InfraBase:
    return base_infra.InfraBase(
        request=request_environment_variable,
        logger_adapter=log,
        configurations=configuration,
    )


def build_http_adapter(configuration: settings.BaseSettings) -> base_infra.InfraBase:
    return base_infra.InfraBase(
        request=request_http,
        logger_adapter=log,
        configurations=configuration,
    )


app = build()
