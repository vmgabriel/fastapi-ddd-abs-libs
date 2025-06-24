from typing import List

import importlib.util
import  pathlib

from src.infra.migrator import model as migrator_model


def all_files(path: pathlib.Path) -> List[pathlib.Path]:
    files = []
    for file in path.iterdir():
        if file.is_file():
            files.append(file)
    return files


def get_migration(path: pathlib.Path) -> migrator_model.Migrator | None:
    spec = importlib.util.spec_from_file_location("migration", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, "migrator", None)


def get_migrate_handler(path: pathlib.Path) -> migrator_model.MigrateHandler | None:
    name_migration = path.name.split(".")[0]
    migration = get_migration(path=path)
    if not migration:
        return None
    return migrator_model.MigrateHandler(name=name_migration, migrator=migration)