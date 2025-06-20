from src import settings
from src.infra.log import logging
from src.infra.migrator import model as migrator_model
from src.infra.migrator import psycopg as migrator_psycopg
from src.infra.uow import psycopg as uow_psycopg


def test_psycopg_migrate() -> None:
    configuration = settings.DevSettings()
    logger = logging.LoggingAdapter(configuration=configuration)
    uow = uow_psycopg.PsycopgUOW(logger=logger, configuration=configuration)
    migration_handler = migrator_psycopg.PsycopgMigrationHandler(
        configuration=configuration,
        logger=logger,
        uow=uow,
    )

    migration_handler.add_migration(
        migrator_model.MigrateHandler(
            name="1_migration_context",
            migrator=migrator_model.Migrator(
                up="",
                rollback="",
            ),
            is_migrated=False,
        )
    )

    assert len(migration_handler.migrations) == 1
    assert migration_handler.migrations[0].name == "1_migration_context"
    assert not migration_handler.migrations[0].is_migrated
