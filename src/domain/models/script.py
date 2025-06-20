import abc
from typing import Any, Dict, List, Type

import pydantic


class ScriptRequirements(pydantic.BaseModel):
    requirements: List[str]


class Script(abc.ABC):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

    @abc.abstractmethod
    def execute(self) -> None:
        raise NotImplementedError()


class ScriptFactory(abc.ABC):
    script: Type[Script]
    request: ScriptRequirements

    def __init__(self, request: ScriptRequirements, script: Type[Script]) -> None:
        self.request = request
        self.script = script

    def inject(self, dependencies: Dict[str, Any]) -> Script:
        return self.script(
            **{
                requirement: dependencies[requirement]
                for requirement in self.request.requirements
            }
        )
