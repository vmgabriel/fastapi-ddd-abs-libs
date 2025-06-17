from __future__ import annotations

from typing import List, Type

from src.fastapi_ddd_abs_libs import base

from . import model, uvicorn

port = Type[model.ServerAdapter]

options: List[base.InfraOption[port]] = [
    base.InfraOption[port](
        title="uvicorn",
        priority=1,
        type_adapter=uvicorn.UvicornAdapter,
    ),
    base.InfraOption[port](
        title="fake",
        priority=2,
        type_adapter=uvicorn.UvicornAdapter,
    ),
]


request: base.InfraRequest[port] = base.InfraRequest[port](
    title="server",
    requirements=["configuration", "http", "logger"],
    options=options,
)
