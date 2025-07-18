import pathlib
from typing import cast

from src.domain import libtools

current_migration_path = pathlib.Path(__file__).parent


migrations = [
    libtools.get_migrate_handler(path=cast(pathlib.Path, file))
    for file in libtools.all_files(path=current_migration_path)
    if file.name != "__init__.py" and file != "."
]

migrations.sort(key=lambda migration: migration.name.split("_")[0] if migration else 0)
