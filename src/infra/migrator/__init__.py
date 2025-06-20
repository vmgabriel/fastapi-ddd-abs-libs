from __future__ import annotations

from typing import List, Type

from src.fastapi_ddd_abs_libs import base

from . import model, psycopg

port = Type[model.MigratorHandler]

options: List[base.InfraOption[port]] = [
    base.InfraOption[port](
        title="psycopg",
        priority=1,
        type_adapter=psycopg.PsycopgMigrationHandler,
    ),
    base.InfraOption[port](
        title="fake",
        priority=2,
        type_adapter=psycopg.PsycopgMigrationHandler,
    ),
]


request: base.InfraRequest[port] = base.InfraRequest[port](
    title="migrator",
    requirements=["configuration", "logger", "uow"],
    options=options,
)
