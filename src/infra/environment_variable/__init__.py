from __future__ import annotations

from typing import List, Type

from src.fastapi_ddd_abs_libs import base

from . import dotenv_python, model

port = Type[model.EnvironmentVariableAdapter]


options: List[base.InfraOption[port]] = [
    base.InfraOption[port](
        title="dotenv-python",
        priority=1,
        type_adapter=dotenv_python.DotEnvPort,
    ),
    base.InfraOption[port](
        title="fake",
        priority=2,
        type_adapter=dotenv_python.DotEnvPort,
    ),
]


request: base.InfraRequest[port] = base.InfraRequest[port](
    title="env",
    requirements=["configuration"],
    options=options,
)
