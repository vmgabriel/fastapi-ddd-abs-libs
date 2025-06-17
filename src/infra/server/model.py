import abc

from src import settings
from src.infra.http import model as http_model
from src.infra.log import model as log_model


class ServerAdapter(abc.ABC):
    http: http_model.HttpModel
    configuration: settings.BaseSettings

    def __init__(
        self,
        http: http_model.HttpModel,
        logger: log_model.LogAdapter,
        configuration: settings.BaseSettings,
    ):
        self.http = http
        self.configuration = configuration
        self.logger = logger

    @abc.abstractmethod
    def execute(self) -> None:
        raise NotImplementedError()
