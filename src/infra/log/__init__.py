from __future__ import annotations

from typing import List, Type

from src.fastapi_ddd_abs_libs import base

from . import logging, model

port = Type[model.LogAdapter]

options: List[base.InfraOption[port]] = [
    base.InfraOption[port](
        title="logging",
        priority=1,
        type_adapter=logging.LoggingAdapter,
    ),
    base.InfraOption[port](
        title="fake",
        priority=2,
        type_adapter=logging.LoggingAdapter,
    ),
]


request: base.InfraRequest[port] = base.InfraRequest[port](
    title="logger",
    requirements=["configuration"],
    options=options,
)
