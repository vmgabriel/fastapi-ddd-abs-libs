from __future__ import annotations

from typing import List, Type

from src.fastapi_ddd_abs_libs import base

from . import cyclopts, model

port = Type[model.CLIModel]

options: List[base.InfraOption[port]] = [
    base.InfraOption[port](
        title="cyclopts",
        priority=1,
        type_adapter=cyclopts.CycloptsCLIModel,
    ),
    base.InfraOption[port](
        title="fake",
        priority=2,
        type_adapter=cyclopts.CycloptsCLIModel,
    ),
]


request: base.InfraRequest[port] = base.InfraRequest[port](
    title="cli",
    requirements=["configuration", "logger"],
    options=options,
)
