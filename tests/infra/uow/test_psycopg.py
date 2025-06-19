from unittest import mock

import psycopg

from src import settings
from src.infra.log import logging
from src.infra.uow import model
from src.infra.uow import psycopg as infra_psycopg


@mock.patch("psycopg.connect")
def test_can_open_close_and_generate_session(connect: mock.MagicMock) -> None:
    configuration = settings.DevSettings()
    logger = logging.LoggingAdapter(configuration)
    adapter: model.UOW = infra_psycopg.PsycopgUOW(
        logger=logger,
        configuration=configuration,
    )

    connect.return_value.__enter__.return_value = mock.MagicMock(
        spec=psycopg.Connection
    )

    assert adapter.session_factory == infra_psycopg.PsycopgSession

    with adapter.session() as session:
        assert session is not None
        assert isinstance(session, infra_psycopg.PsycopgSession)
