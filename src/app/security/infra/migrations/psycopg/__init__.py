import pathlib

from src.domain import libtools

current_migration_path = pathlib.Path(__file__).parent


migrations = [
    libtools.get_migrate_handler(path=file)
    for file in libtools.all_files(path=current_migration_path)
    if file.name != "__init__.py" and file != "."
]
