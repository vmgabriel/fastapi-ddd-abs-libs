from src.domain.entrypoint import cli as entrypoint_cli
from src.domain.entrypoint import model as entrypoint_model

from src.app.security import command as security_command


class CreateSuperUserDocumentationEntrypointCLI(entrypoint_cli.EntrypointCLIDocumentation):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            description = "Create a Super User Client",
            usage = "Usage: create_admin ...",
            *args, **kwargs
        )


class CreateSuperUserEntrypointCLI(entrypoint_cli.EntrypointCLI):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            name="create_admin",
            group="security",
            documentation=CreateSuperUserDocumentationEntrypointCLI(),
            security=entrypoint_model.EntrypointSecurity(),
            cmd=security_command.CreateSuperUserCommand(),
            *args, **kwargs
        )