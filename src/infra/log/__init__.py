from __future__ import annotations

from src.fastapi_ddd_abs_libs import base

from . import logging

options = [
    base.InfraOption(
        title="logging",
        priority=1,
        type_adapter=logging.LoggingAdapter,
    ),
    base.InfraOption(
        title="fake",
        priority=2,
        type_adapter=logging.LoggingAdapter,
    ),
]


request = base.InfraRequest(
    title="logger",
    requirements=["configuration"],
    options=options,
)
