import abc
from typing import List

import pydantic

from src import settings
from src.infra.log import model as log_model
from src.infra.uow import model as log_uow


class MigrationFailedError(Exception):
    message = "Migration not completed"


class MigrationsNotCompletedError(Exception):
    message = "Migrations Not completed"


class Migrator(pydantic.BaseModel):
    up: str
    rollback: str


class MigrateHandler(pydantic.BaseModel):
    name: str
    migrator: Migrator
    is_migrated: bool = False


class MigratorHandler(abc.ABC):
    migrations: List[MigrateHandler]
    logger: log_model.LogAdapter
    uow: log_uow.UOW

    configuration: settings.BaseSettings

    def __init__(
        self,
        configuration: settings.BaseSettings,
        logger: log_model.LogAdapter,
        uow: log_uow.UOW,
    ) -> None:
        self.configuration = configuration
        self.logger = logger
        self.uow = uow

        self.migrations = []

    def add_migration(self, migration: MigrateHandler) -> None:
        self.migrations.append(migration)

    def execute(self) -> None:
        with self.uow.session() as session:
            for to_migrate in self.migrations:
                if not to_migrate:
                    continue
                if self._is_migrated(to_migrate, session):
                    self.logger.info(f"Migration {to_migrate.name} already completed")
                    continue
                try:
                    self.logger.info(f"Making Migrating {to_migrate.name}")
                    self._migrate(to_migrate, session)
                    self._mark_as_migrated(to_migrate, session)
                except MigrationFailedError as exc:
                    self.logger.error(f"Migration {to_migrate.name} failed: {exc}")
                    self.logger.warning(
                        f"Migration {to_migrate.name} failed - Making Rollback"
                    )
                    self._rollback_migration(to_migrate, session)
            session.commit()
            if all(not migration.is_migrated for migration in self.migrations if migration):
                self.logger.info("Not Require Migrations - All Completed")

    def pre_execute(self) -> None:
        with self.uow.session() as session:
            self._check_and_execute_table_base(session)
            session.commit()

    @abc.abstractmethod
    def _check_and_execute_table_base(self, session: log_uow.Session) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def _is_migrated(
        self, to_migrate: MigrateHandler, session: log_uow.Session
    ) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def _mark_as_migrated(
        self, to_migrate: MigrateHandler, session: log_uow.Session
    ) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def _rollback_migration(
        self, to_migrate: MigrateHandler, session: log_uow.Session
    ) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def _migrate(self, to_migrate: MigrateHandler, session: log_uow.Session) -> None:
        raise NotImplementedError()
