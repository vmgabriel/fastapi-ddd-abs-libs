from logging import getLogger
from typing import Any, Dict, List

from src import settings
from src.app.shared import scripts as shared_scripts
from src.domain.models import script as script_domain
from src.fastapi_ddd_abs_libs import base as base_infra
from src.infra.environment_variable import request as request_environment_variable
from src.infra.filter import filter_builder
from src.infra.http import request as request_http
from src.infra.jwt import request as jwt_request
from src.infra.log import request as request_logger
from src.infra.migrator import request as migrator_request
from src.infra.server import model as model_server
from src.infra.server import request as server_request
from src.infra.uow import request as uow_request

log = getLogger(__name__)


def build() -> model_server.ServerAdapter:
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

    dependencies["jwt"] = build_jwt_adapter(configuration).selected_with_configuration(
        dependencies=dependencies
    )

    dependencies["http"] = build_http_adapter(
        configuration
    ).selected_with_configuration(dependencies=dependencies)

    dependencies["server"] = build_server_adapter(
        configuration
    ).selected_with_configuration(dependencies=dependencies)

    dependencies["uow"] = build_uow_adapter(configuration).selected_with_configuration(
        dependencies=dependencies
    )

    dependencies["migrator"] = build_migrator_adapter(
        configuration
    ).selected_with_configuration(dependencies=dependencies)

    dependencies["filter_builder"] = filter_builder

    execute_pre_scripts(dependencies=dependencies, configuration=configuration)

    return dependencies["server"]


def execute_pre_scripts(
    dependencies: Dict[str, Any], configuration: settings.BaseSettings
) -> None:
    pre_scripts: List[script_domain.ScriptFactory] = [
        shared_scripts.MigrationBaseScriptFactory()
    ]

    for pre_script in pre_scripts:
        pre_current_script = pre_script.inject(dependencies=dependencies)
        pre_current_script.execute()


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


def build_server_adapter(configuration: settings.BaseSettings) -> base_infra.InfraBase:
    return base_infra.InfraBase(
        request=server_request,
        logger_adapter=log,
        configurations=configuration,
    )


def build_jwt_adapter(configuration: settings.BaseSettings) -> base_infra.InfraBase:
    return base_infra.InfraBase(
        request=jwt_request,
        logger_adapter=log,
        configurations=configuration,
    )


def build_uow_adapter(configuration: settings.BaseSettings) -> base_infra.InfraBase:
    return base_infra.InfraBase(
        request=uow_request,
        logger_adapter=log,
        configurations=configuration,
    )


def build_migrator_adapter(
    configuration: settings.BaseSettings,
) -> base_infra.InfraBase:
    return base_infra.InfraBase(
        request=migrator_request,
        logger_adapter=log,
        configurations=configuration,
    )


app = build()
