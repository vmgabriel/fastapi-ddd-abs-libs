import datetime

import pydantic

from src.app.security import domain as domain_security
from src.domain.services import user as service_user
from src.infra.jwt import model as jwt_model
from src.infra.log import model as log_model


class AuthenticationResponse(pydantic.BaseModel):
    status: bool = False
    message: str
    type: str | None
    access_token: str | None
    refresh_token: str | None
    generation_datetime: datetime.datetime | None
    expiration_datetime: datetime.datetime | None


_INVALID_AUTHENTICATION = AuthenticationResponse(
    access_token=None,
    refresh_token=None,
    generation_datetime=None,
    expiration_datetime=None,
    message="Invalid Authentication",
    type=None,
)


def _find_user_by_username(
    username: str,
    user_repository: domain_security.UserRepository,
) -> domain_security.UserData | None:
    return user_repository.by_username(username=username)


def authenticate(
    jwt: jwt_model.AuthJWT,
    user_repository: domain_security.UserRepository,
    username: str,
    password: pydantic.SecretStr,
    logger: log_model.LogAdapter,
) -> AuthenticationResponse:
    user_data = _find_user_by_username(
        username=username, user_repository=user_repository
    )
    if not user_data:
        logger.warning(f"User {username} not found")
        return _INVALID_AUTHENTICATION
    if not user_data.is_auth(password=password):
        logger.warning(f"User {username} not authenticated")
        return _INVALID_AUTHENTICATION

    auth_user = service_user.AuthUser(
        id=user_data.id,
        name=user_data.name,
        last_name=user_data.last_name,
        username=user_data.username,
    )

    encoded = jwt.encode(current_user=auth_user, aud=user_data.permissions)

    return AuthenticationResponse(
        status=True,
        message="Valid Authorization",
        type=encoded.type,
        access_token=encoded.access_token,
        refresh_token=encoded.refresh_token,
        generation_datetime=encoded.generation,
        expiration_datetime=encoded.expiration,
    )
