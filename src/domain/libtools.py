import importlib.util
import inspect
import pathlib
import pydantic
from importlib.machinery import ModuleSpec
from types import ModuleType
from typing import List, Type, cast, Any

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


def get_parameters_request(current_class: Type[pydantic.BaseModel]) -> List[ParameterVariable]:
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