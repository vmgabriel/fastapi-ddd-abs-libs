from __future__ import annotations

from src.fastapi_ddd_abs_libs import base

from . import dotenv_python

options = [
    base.InfraOption(
        title="dotenv-python",
        priority=1,
        type_adapter=dotenv_python.DotEnvPort,
    ),
    base.InfraOption(
        title="fake",
        priority=2,
        type_adapter=dotenv_python.DotEnvPort,
    ),
]


request = base.InfraRequest(
    title="env",
    requirements=["configuration"],
    options=options,
)
