from typing import cast

from src.domain.models import repository as repository_model
from src.domain.models.filter import FilterBuilder
from src.domain.services import command
from src.infra.log import model as log_model
from src.infra.uow.model import UOW

from .domain import repository as domain_repository
from .services import board as board_services

# Create - Task


# Get By ID - Task


# Create Board


class CreateBoardCommand(command.Command):
    logger: log_model.LogAdapter
    repository_getter: repository_model.RepositoryGetter
    uow: UOW
    filter_builder: FilterBuilder

    def __init__(self):
        super().__init__(
            requirements=[
                "logger",
                "repository_getter",
                "uow",
                "filter_builder",
            ],
            request_type=board_services.CreateBoardCommandRequest,
        )

    async def execute(self) -> command.CommandResponse:
        self.logger = self._deps["logger"]
        self.repository_getter = cast(
            repository_model.RepositoryGetter, self._deps["repository_getter"]
        )
        self.uow = self._deps["uow"]
        self.filter_builder = self._deps["filter_builder"]

        self.logger.info("Executing CreateBoardCommand")

        if self.parameters.get("version") != "v1":
            raise ValueError("Version not found")

        user_id = self.parameters.get("user")
        if not user_id:
            raise ValueError("User not found")

        if not self.request:
            raise ValueError("Request not found")

        current_request = cast(board_services.CreateBoardCommandRequest, self.request)

        with self.uow.session() as session:
            repository_board = cast(
                domain_repository.BoardRepository,
                self.repository_getter(
                    repository=domain_repository.BoardRepository,
                    session=session,
                ),
            )
            repository_ownership = cast(
                domain_repository.OwnerShipBoardRepository,
                self.repository_getter(
                    repository=domain_repository.OwnerShipBoardRepository,
                    session=session,
                ),
            )

            new_entity_board = board_services.create_board(
                payload=current_request,
                user_id=user_id,
                repository_board=repository_board,
                repository_ownership=repository_ownership,
                logger=self.logger,
            )
            session.commit()

            return command.CommandResponse(
                trace_id=current_request.trace_id,
                payload=new_entity_board.model_dump(),
            )


class GetByIDBoardCommand(command.Command):
    logger: log_model.LogAdapter
    repository_getter: repository_model.RepositoryGetter
    uow: UOW
    filter_builder: FilterBuilder

    def __init__(self):
        super().__init__(
            requirements=[
                "logger",
                "repository_getter",
                "uow",
                "filter_builder",
            ],
            request_type=command.CommandRequest,
        )

    async def execute(self) -> command.CommandResponse:
        self.logger = self._deps["logger"]
        self.repository_getter = cast(
            repository_model.RepositoryGetter, self._deps["repository_getter"]
        )
        self.uow = self._deps["uow"]
        self.filter_builder = self._deps["filter_builder"]

        if self.parameters.get("version") != "v1":
            raise ValueError("Version not found")

        user_id = self.parameters.get("user")
        if not user_id:
            raise ValueError("User not found")

        board_id = self.parameters.get("id")
        if not board_id:
            raise ValueError("Board ID is required")

        with self.uow.session() as session:
            repository_board = cast(
                domain_repository.BoardRepository,
                self.repository_getter(
                    repository=domain_repository.BoardRepository,
                    session=session,
                ),
            )

            repository_ownership = cast(
                domain_repository.OwnerShipBoardRepository,
                self.repository_getter(
                    repository=domain_repository.OwnerShipBoardRepository,
                    session=session,
                ),
            )

            entity_board = board_services.get_myself_board_by_id(
                board_id=board_id,
                user_id=user_id,
                repository_board=repository_board,
                repository_ownership=repository_ownership,
            )

        return command.CommandResponse(
            trace_id=cast(command.CommandRequest, self.request).trace_id,
            payload=getattr(entity_board, "model_dump", lambda: {})(),
        )
