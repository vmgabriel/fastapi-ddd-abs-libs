from __future__ import annotations

from typing import List, Type

from src.fastapi_ddd_abs_libs import base

from . import model, pyjwt

port = Type[model.AuthJWT]

options: List[base.InfraOption[port]] = [
    base.InfraOption[port](
        title="pyjwt",
        priority=1,
        type_adapter=pyjwt.AuthPyJWT,
    ),
    base.InfraOption[port](
        title="fake",
        priority=2,
        type_adapter=pyjwt.AuthPyJWT,
    ),
]


request: base.InfraRequest[port] = base.InfraRequest[port](
    title="jwt",
    requirements=["configuration", "logger"],
    options=options,
)
