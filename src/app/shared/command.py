import uuid

from src.domain.services import command
from src.infra.log import model as log_model


class HealthCheckStatusCommand(command.Command):
    logger: log_model.LogAdapter

    def __init__(self):
        super().__init__(
            requirements=["logger"],
        )

    async def execute(self) -> command.CommandResponse:
        self.logger = self._deps["logger"]
        self.logger.info("Executing HealthCheck")
        return command.CommandResponse(
            trace_id=getattr(self.request, "trace_id", uuid.uuid4()),
            payload={"message": "ok"},
        )
