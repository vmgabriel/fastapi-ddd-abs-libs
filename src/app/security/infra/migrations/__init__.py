from typing import Dict, List, cast

from src.infra.migrator import model as migrator_model

from . import psycopg

migrations: Dict[str, List[migrator_model.MigrateHandler]] = {
    "psycopg": cast(List[migrator_model.MigrateHandler], psycopg.migrations),
}
