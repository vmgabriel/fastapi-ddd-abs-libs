from typing import List
import abc

from src.domain.entrypoint import cli as domain_cli
from src.infra.log import model as log_model

from src import settings


class AppCLI:
    instance: object | None = None

    def __init__(self, instance: object | None = None):
        self.instance = instance

    def __call__(self) -> object:
        return self.instance


class CLIModel(abc.ABC):
    scripts: List[domain_cli.EntrypointCLI]
    
    configuration: settings.BaseSettings
    logger: log_model.LogAdapter
    
    def __init__(
        self, 
        configuration: settings.BaseSettings,
        logger: log_model.LogAdapter,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.configuration = configuration
        self.logger = logger
        self.scripts = []
    
    def add_script(self, script: domain_cli.EntrypointCLI) -> None:
        self.scripts.append(script)
        
    @abc.abstractmethod
    def execute(self) -> AppCLI:
        raise NotImplementedError()