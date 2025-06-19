import abc
from typing import List, TypeVar

from src import settings
from src.domain.entrypoint import http as domain_http
from src.domain.services import command
from src.infra.jwt import model as jwt_model
from src.infra.log import model as log_model

T = TypeVar("T", bound=command.Command)


class AppHttp:
    instance: object | None = None

    def __init__(self, instance: object | None = None):
        self.instance = instance

    def __call__(self) -> object:
        return self.instance


class HttpModel(abc.ABC):
    routes: List[domain_http.EntrypointHttp]

    configuration: settings.BaseSettings
    logger: log_model.LogAdapter

    def __init__(
        self,
        configuration: settings.BaseSettings,
        logger: log_model.LogAdapter,
        jwt: jwt_model.AuthJWT,
    ) -> None:
        self.configuration = configuration
        self.logger = logger
        self.jwt = jwt
        self.routes = []

    def add_route(self, route: domain_http.EntrypointHttp) -> None:
        self.routes.append(route)

    @abc.abstractmethod
    def check_authentication(
        self,
        token: str,
        route: domain_http.EntrypointHttp,
    ) -> jwt_model.StatusCheckJWT:
        raise NotImplementedError()

    @abc.abstractmethod
    def execute(self) -> AppHttp:
        raise NotImplementedError()
