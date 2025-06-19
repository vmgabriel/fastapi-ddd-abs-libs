from logging import getLogger
from typing import cast

from src import settings
from src.domain.entrypoint import http as entrypoint_http
from src.domain.entrypoint import model as entrypoint_model
from src.domain.services import command
from src.fastapi_ddd_abs_libs import base as base_infra
from src.infra.http import model, request
from src.infra.jwt import pyjwt
from src.infra.log import logging
from src.infra.log import model as log_model

logger = getLogger(__name__)


class MyCommandTest(command.Command):
    def __init__(self):
        requirements = ["logger", "configuration"]
        super().__init__(requirements=requirements)

    async def execute(self) -> command.CommandResponse:
        my_log: log_model.LogAdapter = self._deps["logger"]

        my_log.info("this is log intern")

        if not self.request:
            raise NotImplementedError()
        return command.CommandResponse(trace_id=self.request.trace_id)


example_response = entrypoint_http.ExampleEntrypointDocumentationHttp(
    status_code=200,
    description="Success Data of Items",
    content={"a": 1, "b": 2},
    example_name="example_response",
    type=entrypoint_model.ResponseType.JSON,
)


my_doc = entrypoint_http.EntrypointHttpDocumentation(
    summary="this is the summary",
    description="this is the description",
    responses=[example_response],
    tags=["a"],
)


my_entrypoint = entrypoint_http.EntrypointHttp(
    cmd=MyCommandTest(),
    security=entrypoint_model.EntrypointSecurity(),
    route="/a",
    name="my-command-with-a",
    documentation=my_doc,
)


def test_fastapi_add_and_inject_route() -> None:
    configuration = settings.DevSettings()
    logger = logging.LoggingAdapter(configuration)
    http_build: base_infra.InfraBase = base_infra.InfraBase(
        request=request,
        logger_adapter=logger,
        configurations=configuration,
    )
    jwt_adapter = pyjwt.AuthPyJWT(configuration=configuration, logger=logger)

    http_adapter = cast(
        model.HttpModel,
        http_build.select_and_inject(
            "fastapi",
            {"logger": logger, "configuration": configuration, "jwt": jwt_adapter},
        ),
    )

    http_adapter.add_route(my_entrypoint)

    app_executed = http_adapter.execute()

    assert len(http_adapter.routes) == 1
    assert app_executed.instance is not None
