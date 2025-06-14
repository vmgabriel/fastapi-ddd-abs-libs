import pathlib
from typing import Any, Dict

import dotenv

from src import settings

from . import model


class DotEnvPort(model.EnvironmentVariableAdapter):
    obj: dotenv.main.DotEnv

    def __init__(self, configuration: settings.BaseSettings) -> None:
        super().__init__(configuration=configuration)
        path = pathlib.Path() / ".env"
        dotenv.load_dotenv(dotenv_path=path.absolute())
        self.obj = dotenv.main.DotEnv(dotenv_path=path.absolute())

    def get(self, value: str) -> str | None:
        return self.obj.get(key=value)

    def all(self) -> Dict[str, Any]:
        return {k.lower(): v for k, v in self.obj.dict().items()}
