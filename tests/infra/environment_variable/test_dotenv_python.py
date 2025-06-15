import unittest.mock as mock
from logging import getLogger

from src import settings
from src.fastapi_ddd_abs_libs import base as base_infra
from src.infra.environment_variable import model as env_model
from src.infra.environment_variable import request as env_request

logger = getLogger(__name__)


@mock.patch("dotenv.main.DotEnv.dict")
def test_get_environment_ok(
    dict: mock.MagicMock,
) -> None:
    expected_data = {"MODE": "dev", "DEBUG_LEVEL": "info"}
    dict.return_value = expected_data

    configuration = settings.DevSettings()

    env_adapter: base_infra.InfraBase = base_infra.InfraBase(
        request=env_request,
        logger_adapter=logger,
        configurations=configuration,
    )

    environment: env_model.EnvironmentVariableAdapter = (
        env_adapter.selected_with_configuration({"configuration": configuration})
    )

    assert environment.all() == {k.lower(): v for k, v in expected_data.items()}
