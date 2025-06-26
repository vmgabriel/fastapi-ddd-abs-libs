from typing import Dict, List

from src.domain.entrypoint import model as entrypoint_model

from . import http as http_shared

entrypoints: Dict[str, List[entrypoint_model.EntrypointModel]] = {
    "http": [http_shared.GetHealthcheckStatusEntrypointHttp()]
}
