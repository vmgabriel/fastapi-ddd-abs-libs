import unittest.mock as mock

from src import settings
from src.infra.http import fastapi as fastapi_infra
from src.infra.log import logging
from src.infra.server import uvicorn


@mock.patch("uvicorn.run")
def test_get_uvicorn_ok(
    run: mock.MagicMock,
) -> None:
    configuration = settings.DevSettings()
    log = logging.LoggingAdapter(configuration=configuration)
    http = fastapi_infra.FastApiAdapter(configuration=configuration, logger=log)

    adapter = uvicorn.UvicornAdapter(configuration=configuration, http=http, logger=log)
    adapter.execute()

    run.assert_called()
