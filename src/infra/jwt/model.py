import abc
import datetime
from typing import Any, Dict, List, Optional

import pydantic

from src import settings
from src.domain.entrypoint import model as entrypoint_model
from src.domain.services import user
from src.infra.log import model as log_model


class JWTData(pydantic.BaseModel):
    user: user.AuthUser
    aud: List[str]
    gen: datetime.datetime
    exp: datetime.datetime

    def has_permission(self, audiences: List[str]) -> bool:
        print("audiences", audiences)
        print("aud", self.aud)
        role = list(filter(lambda aud: aud.startswith("role:"), self.aud))[0]
        all_audiences_with_role = user.ROLE_PERMISSIONS[user.Role(role)]
        current_user_audiences = [
            user.Audience(aud) for aud in self.aud if user.Audience.exists(aud)
        ] + all_audiences_with_role
        return any(user.Audience(aud) in current_user_audiences for aud in audiences)

    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        return {
            "user": self.user.model_dump(),
            "aud": self.aud,
            "gen": self.gen.timestamp(),
            "exp": self.exp.timestamp(),
        }


class RefreshAuthUser(pydantic.BaseModel):
    id: str
    gen: datetime.datetime
    exp: datetime.datetime

    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        return {
            "id": self.id,
            "gen": self.gen.timestamp(),
            "exp": self.exp.timestamp(),
        }


class StatusCheckJWT(pydantic.BaseModel):
    message: str
    status: bool = False
    type: entrypoint_model.StatusType = entrypoint_model.StatusType.OK
    data: Optional[JWTData | RefreshAuthUser] = None


class EncodedJWT(pydantic.BaseModel):
    type: str
    access_token: str
    refresh_token: str
    generation: datetime.datetime
    expiration: datetime.datetime


class AuthJWT(abc.ABC):
    configuration: settings.BaseSettings
    logger: log_model.LogAdapter

    def __init__(
        self, configuration: settings.BaseSettings, logger: log_model.LogAdapter
    ) -> None:
        self.configuration = configuration
        self.logger = logger

    @abc.abstractmethod
    def encode(
        self,
        current_user: user.AuthUser,
        aud: List[str],
        expiration: Optional[datetime.timedelta] = None,
    ) -> EncodedJWT:
        raise NotImplementedError()

    @abc.abstractmethod
    def check_and_decode(self, token: str, allowed_aud: List[str]) -> StatusCheckJWT:
        raise NotImplementedError()

    @abc.abstractmethod
    def check_refresh_and_decode(self, token: str) -> StatusCheckJWT:
        raise NotImplementedError()
