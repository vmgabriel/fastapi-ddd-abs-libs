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
        http_task.AddMemberBoardEntrypointHttp(),
        http_task.RemoveMemberBoardEntrypointHttp(),
        http_task.UpdateRoleMemberBoardEntrypointHttp(),
        http_task.ListTaskEntrypointHttp(),
        http_task.CreateTaskEntrypointHttp(),
        http_task.GetByIDTaskEntrypointHttp(),
        http_task.UpdateTaskEntrypointHttp(),
        http_task.DeleteTaskEntrypointHttp(),
        http_task.ListTasksEntrypointHttp(),
    ],
}
