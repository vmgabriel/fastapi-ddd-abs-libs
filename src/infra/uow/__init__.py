from __future__ import annotations

from typing import List, Type

from src.fastapi_ddd_abs_libs import base

from . import model, psycopg

port = Type[model.UOW]

options: List[base.InfraOption[port]] = [
    base.InfraOption[port](
        title="psycopg",
        priority=1,
        type_adapter=psycopg.PsycopgUOW,
    ),
    base.InfraOption[port](
        title="fake",
        priority=2,
        type_adapter=psycopg.PsycopgUOW,
    ),
]


request: base.InfraRequest[port] = base.InfraRequest[port](
    title="uow",
    requirements=["configuration", "logger", "session_factory"],
    options=options,
)
