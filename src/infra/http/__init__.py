from __future__ import annotations

from typing import List, Type

from src.fastapi_ddd_abs_libs import base

from . import fastapi, model

port = Type[model.HttpModel]

options: List[base.InfraOption[port]] = [
    base.InfraOption[port](
        title="fastapi",
        priority=1,
        type_adapter=fastapi.FastApiAdapter,
    ),
    base.InfraOption[port](
        title="fake",
        priority=2,
        type_adapter=fastapi.FastApiAdapter,
    ),
]


request: base.InfraRequest[port] = base.InfraRequest[port](
    title="http",
    requirements=["configuration", "logger"],
    options=options,
)
