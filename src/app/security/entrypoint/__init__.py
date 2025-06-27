from typing import Dict, List

from src.domain.entrypoint import model as entrypoint_model

from . import http as http_security, cli as cli_security

entrypoints: Dict[str, List[entrypoint_model.EntrypointModel]] = {
    "http": [http_security.GetDataEntrypointHttp()],
}

scripts: Dict[str, List[entrypoint_model.EntrypointModel]] = {
    "cli": [cli_security.CreateSuperUserEntrypointCLI()],
}
