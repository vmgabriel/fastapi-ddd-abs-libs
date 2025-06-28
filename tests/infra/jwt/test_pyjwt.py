from src import settings
from src.domain.entrypoint import model as entrypoint_model
from src.domain.services import user
from src.infra.jwt import pyjwt
from src.infra.log import logging

_TEST_TOKEN = (
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmF"
    "tZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTc1MDI5MzAyMywiZXhwIjox"
    "NzUwMjk2NjIzfQ.olMdxu-VlIgCGD4SvX4XrY_hGAy6IxKaUmkEcPh-CBM"
)


def test_pyjwt_check_authentication_ok() -> None:
    configuration = settings.DevSettings()
    configuration.auth_access_token_secret = "123"
    configuration.auth_refresh_token_secret = "123"
    logger = logging.LoggingAdapter(configuration)
    jwt_adapter = pyjwt.AuthPyJWT(configuration=configuration, logger=logger)

    token_model = jwt_adapter.encode(
        current_user=user.AuthUser(
            id="1", name="Gabriel", last_name="Vargas", username="vmgabriel"
        ),
        aud=["role:admin"],
    )

    status_check = jwt_adapter.check_and_decode(
        token=token_model.access_token, allowed_aud=["profile:get"]
    )

    assert status_check.type is entrypoint_model.StatusType.OK


def test_pyjwt_check_authentication_fail() -> None:
    configuration = settings.DevSettings()
    configuration.auth_access_token_secret = "123"
    configuration.auth_refresh_token_secret = "123"
    logger = logging.LoggingAdapter(configuration)
    jwt_adapter = pyjwt.AuthPyJWT(configuration=configuration, logger=logger)

    status_check = jwt_adapter.check_and_decode(
        token=_TEST_TOKEN, allowed_aud=["profile:get"]
    )

    assert status_check.type is entrypoint_model.StatusType.NOT_COMPLETE


def test_pyjwt_encode_ok() -> None:
    configuration = settings.DevSettings()
    configuration.auth_access_token_secret = "123"
    configuration.auth_refresh_token_secret = "123"
    logger = logging.LoggingAdapter(configuration)
    jwt_adapter = pyjwt.AuthPyJWT(configuration=configuration, logger=logger)

    token_model = jwt_adapter.encode(
        current_user=user.AuthUser(
            id="1", name="Gabriel", last_name="Vargas", username="vmgabriel"
        ),
        aud=["role:admin"],
    )

    assert token_model.access_token
    assert token_model.refresh_token
