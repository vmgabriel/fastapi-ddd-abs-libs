import datetime
import pathlib

from src.infra.uow import model as log_uow

from .. import model

EXIST_TABLE_BASE_SQL = "exist_table_select_migration.sql"
MIGRATION_TABLE_BASE_SQL = "migration_table_select_migration.sql"
FIND_FILENAME_IN_MIGRATION_SQL = "find_filename_in_migration_migration.sql"
MARK_AS_MIGRATED_SQL = "mark_as_migrated.sql"


class PsycopgMigrationHandler(model.MigratorHandler):
    exist_table_base_sql_path: pathlib.Path
    migration_table_base_sql_path: pathlib.Path
    find_filename_in_migration_sql_path: pathlib.Path
    mark_as_migrated_sql_path: pathlib.Path

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        _path_sql = "sql"

        sql_path = pathlib.Path(__file__).parent / _path_sql

        self.exist_table_base_sql_path = sql_path / EXIST_TABLE_BASE_SQL
        self.migration_table_base_sql_path = sql_path / MIGRATION_TABLE_BASE_SQL
        self.find_filename_in_migration_sql_path = (
            sql_path / FIND_FILENAME_IN_MIGRATION_SQL
        )
        self.mark_as_migrated_sql_path = sql_path / MARK_AS_MIGRATED_SQL

    def _get_sql(self, file_path: pathlib.Path) -> str:
        return file_path.read_text()

    def _is_migrated(
        self, to_migrate: model.MigrateHandler, session: log_uow.Session
    ) -> bool:
        response_query = session.atomic_execute(
            params=(to_migrate.name,),
            query=self._get_sql(file_path=self.find_filename_in_migration_sql_path),
        )
        return getattr(response_query, "fetchone", lambda: None)() is not None

    def _mark_as_migrated(
        self, to_migrate: model.MigrateHandler, session: log_uow.Session
    ) -> None:
        current_date = datetime.datetime.now()
        session.atomic_execute(
            params=(to_migrate.name, current_date.isoformat()),
            query=self._get_sql(file_path=self.mark_as_migrated_sql_path),
        )
        self.logger.info("Marked as migrated: %s" % to_migrate.name)

    def _rollback_migration(
        self, to_migrate: model.MigrateHandler, session: log_uow.Session
    ) -> None:
        if not to_migrate.is_migrated:
            self.logger.info(f"{to_migrate.name} No require rollback")
        session.atomic_execute(query=to_migrate.migrator.rollback, params=tuple())
        self.logger.info("Rolling back migrate: %s" % to_migrate.name)

    def _migrate(
        self, to_migrate: model.MigrateHandler, session: log_uow.Session
    ) -> None:
        print(f"up {to_migrate.name}")
        session.atomic_execute(query=to_migrate.migrator.up, params=tuple())
        to_migrate.is_migrated = True

    def _check_and_execute_table_base(self, session: log_uow.Session) -> None:
        print("Checking Table of Migration")
        query = self._get_sql(file_path=self.exist_table_base_sql_path)
        response_query = session.atomic_execute(
            params=tuple(),
            query=query,
        )
        if getattr(response_query, "fetchone", lambda: None)() is not None:
            self.logger.info("Initial Migration has already been executed")
            return

        self.logger.info("Require Initial Migration")
        session.atomic_execute(
            query=self._get_sql(file_path=self.migration_table_base_sql_path),
            params=tuple(),
        )
