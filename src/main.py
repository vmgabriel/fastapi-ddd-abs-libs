from logging import getLogger
from typing import Dict, cast

from src import settings
from src.fastapi_ddd_abs_libs import base as base_infra
from src.infra.environment_variable import model as model_env
from src.infra.environment_variable import request as request_environment_variable
from src.infra.log import request as request_logger

log = getLogger(__name__)


_CONFIGURATION = settings.DevSettings()


LOGGER_ADAPTER = base_infra.InfraBase(
    request=request_logger,
    logger_adapter=log,
    configurations=_CONFIGURATION,
)

ENV_ADAPTER = base_infra.InfraBase(
    request=request_environment_variable,
    logger_adapter=log,
    configurations=_CONFIGURATION,
)

dependencies: Dict[str, object] = {
    "configuration": _CONFIGURATION,
}

env_dependency = cast(
    model_env.EnvironmentVariableAdapter,
    ENV_ADAPTER.selected_with_configuration(dependencies=dependencies),
)
_CONFIGURATION.inject(env_dependency.all())

dependencies.update(
    {
        "logger": LOGGER_ADAPTER.selected_with_configuration(dependencies=dependencies),
        "env": env_dependency,
    }
)
