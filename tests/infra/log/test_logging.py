import unittest.mock as mock
from logging import getLogger
from typing import Type

import pytest

from src import settings
from src.fastapi_ddd_abs_libs import base as base_infra
from src.infra.log import model
from src.infra.log import request as request_log

logger = getLogger(__name__)


@mock.patch("logging.Logger._log")
@pytest.mark.parametrize("port", ["fake", "logging", "error"])
def test_get_log(
    _log: mock.MagicMock,
    port: str,
) -> None:
    configuration = settings.DevSettings()

    logger_adapter: base_infra.InfraBase = base_infra.InfraBase[model.LogAdapter](
        request=request_log,
        logger_adapter=logger,
        configurations=configuration,
    )

    if port == "error":
        with pytest.raises(ValueError):
            logger_adapter.select(option=port)
        return
    else:
        log: Type[model.LogAdapter] = logger_adapter.select(option=port)
    execution: model.LogAdapter | None = log(configuration=configuration)

    assert execution

    execution.critical("critical")
    execution.error("Error")
    execution.warning("warning")
    execution.info("Execution with context")

    assert _log.call_count == 4
