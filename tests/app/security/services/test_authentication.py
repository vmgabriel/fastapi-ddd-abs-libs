import datetime
from unittest.mock import MagicMock, Mock

import pytest
from pydantic import SecretStr

from src.app.security.domain import UserData, UserRepository
from src.app.security.services import authentication as authentication_service
from src.domain import libtools
from src.infra.jwt.model import AuthJWT
from src.infra.log.model import LogAdapter


@pytest.fixture
def mock_user_repository():
    return MagicMock(spec=UserRepository)


@pytest.fixture
def mock_jwt():
    return MagicMock(spec=AuthJWT)


@pytest.fixture
def mock_logger():
    return MagicMock(spec=LogAdapter)


def test_authenticate_valid_user(mock_user_repository, mock_jwt, mock_logger):
    username = "valid_user"
    password = SecretStr("correct_password")
    expect_user_data = UserData(
        name="nn_name",
        last_name="ll_name",
        username=username,
        email="as@test.co",
        id="id",
        password=password,
        permissions=["role:admin"],
    )
    _find_user_by_username = MagicMock(spec=UserData)
    _find_user_by_username.return_value = expect_user_data
    libtools.check_password = MagicMock(spec=bool)

    mock_user_repository.by_username.return_value = expect_user_data
    mock_jwt.encode.return_value = MagicMock(
        type="Bearer",
        access_token="access_token",
        refresh_token="refresh_token",
        generation="2025-07-15T00:00:00",
        expiration="2025-07-15T01:00:00",
    )

    result = authentication_service.authenticate(
        jwt=mock_jwt,
        user_repository=mock_user_repository,
        username=username,
        password=password,
        logger=mock_logger,
    )

    assert result.status is True
    assert result.message == "Valid Authorization"
    assert result.type == "Bearer"
    assert result.access_token == "access_token"


def test_authenticate_invalid_username(mock_user_repository, mock_jwt, mock_logger):
    username = "invalid_user"
    password = SecretStr("some_password")

    mock_user_repository.by_username.return_value = None

    result = authentication_service.authenticate(
        jwt=mock_jwt,
        user_repository=mock_user_repository,
        username=username,
        password=password,
        logger=mock_logger,
    )

    assert result.status is False
    assert result.message == "Invalid Authentication"
    mock_logger.warning.assert_called_once_with("User invalid_user not found")


def test_authenticate_invalid_password(mock_user_repository, mock_jwt, mock_logger):
    username = "valid_user"
    password = SecretStr("wrong_password")
    UserData(
        name="nn_name",
        last_name="ll_name",
        username=username,
        email="as@test.co",
        id="id",
        password=password,
        permissions=["role:admin"],
    )
    user_data = MagicMock(spec=UserData)
    user_data.is_auth.return_value = False

    mock_user_repository.by_username.return_value = user_data

    result = authentication_service.authenticate(
        jwt=mock_jwt,
        user_repository=mock_user_repository,
        username=username,
        password=password,
        logger=mock_logger,
    )

    assert result.status is False
    assert result.message == "Invalid Authentication"
    mock_logger.warning.assert_called_once_with("User valid_user not authenticated")


def test_authenticate_jwt_encoding_error(mock_user_repository, mock_jwt, mock_logger):
    username = "valid_user"
    password = SecretStr("correct_password")
    expect_user_data = UserData(
        name="nn_name",
        last_name="ll_name",
        username=username,
        email="as@test.co",
        id="id",
        password=password,
        permissions=["role:admin"],
    )
    user_data = MagicMock(spec=UserData)
    user_data.is_auth.return_value = True

    mock_user_repository.by_username.return_value = expect_user_data
    mock_jwt.encode.side_effect = Exception("JWT encoding error")

    with pytest.raises(Exception, match="JWT encoding error"):
        authentication_service.authenticate(
            jwt=mock_jwt,
            user_repository=mock_user_repository,
            username=username,
            password=password,
            logger=mock_logger,
        )


def test_refresh_token_valid(mock_user_repository, mock_jwt, mock_logger):
    mock_refresh_token = "valid_refresh_token"

    mock_jwt.check_refresh_and_decode.return_value = MagicMock(
        status=True,
        data=Mock(id="123"),
    )
    mock_user_repository.get_by_id.return_value = Mock(
        id="123",
        name="John",
        last_name="Doe",
        username="johndoe",
        permissions=["read", "write"],
    )
    mock_jwt.encode.return_value = Mock(
        type="Bearer",
        access_token="new_access_token",
        refresh_token="new_refresh_token",
        generation="2025-07-15T12:00:00",
        expiration="2025-07-15T15:00:00",
    )

    response = authentication_service.refresh_token(
        jwt=mock_jwt,
        user_repository=mock_user_repository,
        refresh_token=mock_refresh_token,
        logger=mock_logger,
    )

    assert isinstance(response, authentication_service.AuthenticationResponse)
    assert response.status is True
    assert response.message == "Valid Authorization"
    assert response.type == "Bearer"
    assert response.access_token == "new_access_token"
    assert response.refresh_token == "new_refresh_token"
    assert response.generation_datetime == datetime.datetime.fromisoformat(
        "2025-07-15T12:00:00"
    )
    assert response.expiration_datetime == datetime.datetime.fromisoformat(
        "2025-07-15T15:00:00"
    )


def test_refresh_token_invalid(mock_user_repository, mock_jwt, mock_logger):
    mock_refresh_token = "invalid_refresh_token"

    mock_jwt.check_refresh_and_decode.return_value = Mock(status=False, data=None)

    response = authentication_service.refresh_token(
        jwt=mock_jwt,
        user_repository=mock_user_repository,
        refresh_token=mock_refresh_token,
        logger=mock_logger,
    )

    assert isinstance(response, authentication_service.AuthenticationResponse)
    assert response.status is False
    assert response.message == "Invalid Refresh"
    assert response.type is None
    assert response.access_token is None
    assert response.refresh_token is None
    assert response.generation_datetime is None
    assert response.expiration_datetime is None


def test_refresh_token_user_not_found(mock_user_repository, mock_jwt, mock_logger):
    mock_refresh_token = "valid_refresh_token_with_invalid_user"

    mock_jwt.check_refresh_and_decode.return_value = Mock(
        status=True,
        data=Mock(id="invalid_user_id"),
    )
    mock_user_repository.get_by_id.return_value = None

    response = authentication_service.refresh_token(
        jwt=mock_jwt,
        user_repository=mock_user_repository,
        refresh_token=mock_refresh_token,
        logger=mock_logger,
    )

    assert isinstance(response, authentication_service.AuthenticationResponse)
    assert response.status is False
    assert response.message == "Invalid Refresh"
    assert response.type is None
    assert response.access_token is None
    assert response.refresh_token is None
    assert response.generation_datetime is None
    assert response.expiration_datetime is None
