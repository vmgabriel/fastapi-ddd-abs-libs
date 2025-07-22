from typing import Dict, List

from src.domain.entrypoint import model as entrypoint_model

from . import http as http_task

entrypoints: Dict[str, List[entrypoint_model.EntrypointModel]] = {
    "http": [
        http_task.CreateBoardEntrypointHttp(),
        http_task.GetByIDBoardEntrypointHttp(),
        http_task.ListBoardEntrypointHttp(),
        http_task.UpdateBoardEntrypointHttp(),
        http_task.DeleteBoardEntrypointHttp(),
    ],
}
