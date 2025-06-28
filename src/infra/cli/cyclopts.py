import getpass
from typing import Dict, Any, Type

import cyclopts
import pydantic

from src.domain import libtools
from src.domain.entrypoint import cli as entrypoint_cli
from . import model


class CycloptsCLIModel(model.CLIModel):
    app: cyclopts.App

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.app = cyclopts.App(
            name=self.configuration.title,
            help=self.configuration.summary,
        )

    def _print_object_getter(self, object: Type[pydantic.BaseModel]) -> Dict[str, Any]:
        data = {}
        for parameter in libtools.get_parameters_request(object):
            message = f"{parameter.name} - {parameter.type}"
            if parameter.default:
                message += f" [{parameter.default}]"
            if parameter.required:
                message += f" (required)"
            message += ": "
            if parameter.type == pydantic.SecretStr:
                value = getpass.getpass(message)
            else:
                value = input(message)
            if not value and parameter.required:
                raise ValueError(f"Parameter {parameter.name} is required")
            if not value and not parameter.required and parameter.default is not None:
                continue
            data[parameter.name] = parameter.type(value)
        return data

    def _inject_script(self, script: entrypoint_cli.EntrypointCLI) -> None:
        built_command = self.app.command(
            name=script.name,
            group=script.group,
            usage=script.documentation.usage,
        )

        @built_command
        async def executor_script() -> None:
            print(f"Executing Script {script.name}")
            print("_" * 30)
            request = self._print_object_getter(object=script.cmd.request_type)
            print("_" * 30)

            script.cmd.inject_using_dict(request)
            response = await script.cmd.execute()

            print("_" * 30)
            print(f"Response: {response.model_dump()}")

    def _inject_scripts(self) -> None:
        for script in self.scripts:
            self._inject_script(script)

    def execute(self) -> model.AppCLI:
        self._inject_scripts()
        return model.AppCLI(instance=self.app)
