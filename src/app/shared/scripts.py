from src.domain.models import script
from src.infra.log import model as log_model
from src.infra.migrator import model as migrator_model
from src.infra.uow import model as uow_model


class MigrationBaseScriptHandler(script.Script):
    def __init__(
        self,
        logger: log_model.LogAdapter,
        uow: uow_model.UOW,
        migrator: migrator_model.MigratorHandler,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.logger = logger
        self.uow = uow
        self.migrator = migrator

    def execute(self) -> None:
        self.logger.info("Executing MigrationBaseScriptHandler script")
        self.migrator.pre_execute()
        self.logger.info("Executed MigrationBaseScriptHandler script")


class MigrationBaseScriptFactory(script.ScriptFactory):
    def __init__(self) -> None:
        super().__init__(
            script=MigrationBaseScriptHandler,
            request=script.ScriptRequirements(
                requirements=["logger", "uow", "migrator"]
            ),
        )