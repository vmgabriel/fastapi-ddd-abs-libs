from typing import Dict, List

from src.domain.entrypoint import model as entrypoint_model

from . import cli as cli_security
from . import http as http_security

entrypoints: Dict[str, List[entrypoint_model.EntrypointModel]] = {
    "http": [
        http_security.GetDataEntrypointHttp(),
        http_security.AuthenticateEntrypointHttp(),
        http_security.RefreshTokenEntrypointHttp(),
        http_security.CreateUserEntrypointHttp(),
    ],
}

scripts: Dict[str, List[entrypoint_model.EntrypointModel]] = {
    "cli": [cli_security.CreateSuperUserEntrypointCLI()],
}
