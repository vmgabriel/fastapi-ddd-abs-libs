import importlib.util
import inspect
import pathlib
from importlib.machinery import ModuleSpec
from typing import Any, List, Type, cast

import bcrypt
import pydantic

from src.infra.migrator import model as migrator_model


class ParameterVariable(pydantic.BaseModel):
    name: str
    type: Type
    default: Any
    required: bool
    description: str | None


def all_files(path: pathlib.Path) -> List[pathlib.Path]:
    files = []
    for file in path.iterdir():
        if file.is_file():
            files.append(file)
    return files


def get_migration(path: pathlib.Path) -> migrator_model.Migrator | None:
    try:
        spec = cast(
            ModuleSpec, importlib.util.spec_from_file_location("migration", path)
        )
        if spec is None or spec.loader is None:
            return None

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, "migrator", None)
    except Exception as e:
        print(f"Error loading migration from {path}: {e}")
        return None


def get_migrate_handler(path: pathlib.Path) -> migrator_model.MigrateHandler | None:
    name_migration = path.name.split(".")[0]
    migration = get_migration(path=path)
    if not migration:
        return None
    return migrator_model.MigrateHandler(name=name_migration, migrator=migration)


def get_mro_class(obj: Type[object]) -> List[Type[object]]:
    return cast(List[Type[object]], list(inspect.getmro(obj)))


def get_parameters_request(
    current_class: Type[pydantic.BaseModel],
) -> List[ParameterVariable]:
    parameters = []
    for field_name, field in current_class.model_fields.items():
        parameters.append(
            ParameterVariable(
                name=field_name,
                type=field.annotation,
                description=field.description,
                default=field.default,
                required=field.is_required(),
            )
        )
    return parameters


def encrypt_password(password: str) -> str:
    return bcrypt.hashpw(str.encode(password), bcrypt.gensalt()).decode("utf-8")
