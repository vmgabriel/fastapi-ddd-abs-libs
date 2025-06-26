import importlib.util
import inspect
import pathlib
from importlib.machinery import ModuleSpec
from types import ModuleType
from typing import List, Type, cast

from src.infra.migrator import model as migrator_model


def all_files(path: pathlib.Path) -> List[pathlib.Path]:
    files = []
    for file in path.iterdir():
        if file.is_file():
            files.append(file)
    return files


def get_migration(path: pathlib.Path) -> migrator_model.Migrator | None:
    spec = cast(ModuleSpec, importlib.util.spec_from_file_location("migration", path))
    module = importlib.util.module_from_spec(cast(ModuleSpec, spec))
    getattr(spec, "loader.exec_module", lambda x: None)(cast(ModuleType, module))
    return getattr(module, "migrator", None)


def get_migrate_handler(path: pathlib.Path) -> migrator_model.MigrateHandler | None:
    name_migration = path.name.split(".")[0]
    migration = get_migration(path=path)
    if not migration:
        return None
    return migrator_model.MigrateHandler(name=name_migration, migrator=migration)


def get_mro_class(obj: Type[object]) -> List[Type[object]]:
    return cast(List[Type[object]], list(inspect.getmro(obj)))
