from logging import getLogger
from typing import Any, Dict, List

from src import settings
from src.app import security as security_app, shared as shared_app

# domain - apps
from src.app.shared import scripts as shared_scripts
from src.domain.models import domain
from src.domain.models import script as script_domain
from src.fastapi_ddd_abs_libs import base as base_infra

# infra
from src.infra.environment_variable import request as request_environment_variable
from src.infra.filter import filter_builder
from src.infra.http import request as request_http
from src.infra.jwt import request as jwt_request
from src.infra.log import request as request_logger
from src.infra.migrator import request as migrator_request
from src.infra.server import model as model_server
from src.infra.server import request as server_request
from src.infra.uow import request as uow_request
from src.infra.cli import request as cli_request
from src.infra.cli import model as model_cli

log = getLogger(__name__)
apps: List[domain.DomainFactory] = [
    security_app.domain_security,
    shared_app.domain_shared,
]


def _build() -> Dict[str, Any]:
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

    dependencies["uow"] = build_uow_adapter(configuration).selected_with_configuration(
        dependencies=dependencies
    )

    dependencies["migrator"] = build_migrator_adapter(
        configuration
    ).selected_with_configuration(dependencies=dependencies)

    dependencies["filter_builder"] = filter_builder

    dependencies["repository_getter"] = build_repository_getter(
        configuration=configuration, dependencies=dependencies
    )

    dependencies["http"] = build_http_adapter(
        configuration
    ).selected_with_configuration(dependencies=dependencies)

    integrate_http_entrypoints(dependencies=dependencies, configuration=configuration)

    dependencies["server"] = build_server_adapter(
        configuration
    ).selected_with_configuration(dependencies=dependencies)
    
    dependencies["cli"] = build_cli_adapter(
        configuration=configuration
    ).selected_with_configuration(dependencies=dependencies)
    
    integrate_cli_entrypoints(dependencies=dependencies, configuration=configuration)

    execute_migrations(dependencies=dependencies, configuration=configuration)
    execute_pre_scripts(dependencies=dependencies, configuration=configuration)

    return dependencies


def generate_http_server() -> model_server.ServerAdapter:
    dependencies = _build()
    return dependencies["server"]


def generate_cli_server() -> model_cli.AppCLI:
    dependencies = _build()
    return dependencies["cli"].execute()


def execute_pre_scripts(
    dependencies: Dict[str, Any], configuration: settings.BaseSettings
) -> None:
    pre_scripts: List[script_domain.ScriptFactory] = [
        shared_scripts.MigrationBaseScriptFactory()
    ]

    for pre_script in pre_scripts:
        pre_current_script = pre_script.inject(dependencies=dependencies)
        pre_current_script.execute()


def execute_migrations(
    dependencies: Dict[str, Any], configuration: settings.BaseSettings
) -> None:
    migrator = dependencies["migrator"]
    logger = dependencies["logger"]

    logger.info("Executing Migrations")
    for app in apps:
        logger.info(f"Adding Migrations for {app.title}")
        builder = domain.DomainBuilder(
            configuration=configuration,
            logger=logger,
            domain_factory=app,
        )
        for migration in builder.get_migrations():
            migrator.add_migration(migration)

    migrator.execute()


def integrate_http_entrypoints(
    configuration: settings.BaseSettings,
    dependencies: Dict[str, Any],
) -> None:
    logger = dependencies["logger"]
    http = dependencies["http"]
    logger.info("Integrating Http Entrypoints")
    for app in apps:
        logger.info(f"Integrating Http Entrypoints for {app.title}")
        builder = domain.DomainBuilder(
            configuration=configuration,
            logger=logger,
            domain_factory=app,
        )
        for entrypoint in builder.get_entrypoints("http"):
            entrypoint.cmd.inject_dependencies(infra_dependencies=dependencies)
            http.add_route(entrypoint)


def integrate_cli_entrypoints(
    configuration: settings.BaseSettings,
    dependencies: Dict[str, Any],
) -> None:
    logger = dependencies["logger"]
    cli = dependencies["cli"]
    logger.info("Integrating Cli Entrypoints")
    for app in apps:
        logger.info(f"Integrating Cli Entrypoints for {app.title}")
        builder = domain.DomainBuilder(
            configuration=configuration,
            logger=logger,
            domain_factory=app,
        )
        for script in builder.get_scripts("cli"):
            script.cmd.inject_dependencies(infra_dependencies=dependencies)
            cli.add_script(script)



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


def build_repository_getter(
    configuration: settings.BaseSettings,
    dependencies: Dict[str, Any],
):
    logger = dependencies["logger"]
    logger.info("Building Repository Getters")
    repository_getter = domain.RepositoryGetter(repositories=[])
    for app in apps:
        logger.info(f"Building Repository Getters for {app.title}")
        builder = domain.DomainBuilder(
            configuration=configuration,
            logger=dependencies["logger"],
            domain_factory=app,
        )
        repository_getter += builder.get_repositories()
    return repository_getter


def build_cli_adapter(
    configuration: settings.BaseSettings,
) -> base_infra.InfraBase:
    return base_infra.InfraBase(
        request=cli_request,
        logger_adapter=log,
        configurations=configuration,
    )