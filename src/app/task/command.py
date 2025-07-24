from typing import cast

from src.app.security import domain as domain_security
from src.domain.models import repository as repository_model
from src.domain.models.filter import FilterBuilder
from src.domain.services import command
from src.infra.log import model as log_model
from src.infra.uow.model import UOW

from .domain import repository as domain_repository
from .domain.entity import RoleMemberType
from .services import board as board_services
from .services import task as task_services


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


class ListBoardCommand(command.Command):
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

        if not self.request:
            raise ValueError("Request not found")

        with self.uow.session() as session:
            repositor_view_board = cast(
                domain_repository.DetailedBoardRepository,
                self.repository_getter(
                    repository=domain_repository.DetailedBoardRepository,
                    session=session,
                ),
            )

            entity_board = board_services.paginate_myself_board(
                user_id=user_id,
                query=cast(command.CommandQueryRequest, self.request),
                repository_view_detailed_board=repositor_view_board,
                filter_builder=self.filter_builder,
            )

        return command.CommandResponse(
            trace_id=cast(command.CommandRequest, self.request).trace_id,
            payload=getattr(entity_board, "model_dump", lambda: {})(),
        )


class UpdateBoardCommand(command.Command):
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
            request_type=board_services.UpdateBoardCommandRequest,
        )

    async def execute(self) -> command.CommandResponse:
        self.logger = self._deps["logger"]
        self.repository_getter = cast(
            repository_model.RepositoryGetter, self._deps["repository_getter"]
        )
        self.uow = self._deps["uow"]
        self.filter_builder = self._deps["filter_builder"]

        self.logger.info("Executing UpdateBoardCommand")

        if self.parameters.get("version") != "v1":
            raise ValueError("Version not found")

        user_id = self.parameters.get("user")
        if not user_id:
            raise ValueError("User not found")

        board_id = self.parameters.get("id")
        if not board_id:
            raise ValueError("Board not found")

        if not self.request:
            raise ValueError("Request not found")

        current_request = cast(board_services.UpdateBoardCommandRequest, self.request)

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

            update_entity_board = board_services.update_board(
                payload=current_request,
                user_id=user_id,
                board_id=board_id,
                repository_board=repository_board,
                repository_ownership=repository_ownership,
                logger=self.logger,
            )
            session.commit()

        return command.CommandResponse(
            trace_id=current_request.trace_id,
            payload=update_entity_board.model_dump(),
        )


class DeleteBoardCommand(command.Command):
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

        self.logger.info("Executing UpdateBoardCommand")

        if self.parameters.get("version") != "v1":
            raise ValueError("Version not found")

        user_id = self.parameters.get("user")
        if not user_id:
            raise ValueError("User not found")

        board_id = self.parameters.get("id")
        if not board_id:
            raise ValueError("Board not found")

        if not self.request:
            raise ValueError("Request not found")

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

            entity_board = board_services.delete_board(
                user_id=user_id,
                board_id=board_id,
                repository_board=repository_board,
                repository_ownership=repository_ownership,
                logger=self.logger,
            )
            session.commit()

        return command.CommandResponse(
            trace_id=cast(command.CommandRequest, self.request).trace_id,
            payload=entity_board.model_dump(),
        )


class AddMemberCommandRequest(command.CommandRequest):
    user_id: str


class AddMemberBoardCommand(command.Command):
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
            request_type=AddMemberCommandRequest,
        )

    async def execute(self) -> command.CommandResponse:
        self.logger = self._deps["logger"]
        self.repository_getter = cast(
            repository_model.RepositoryGetter, self._deps["repository_getter"]
        )
        self.uow = self._deps["uow"]
        self.filter_builder = self._deps["filter_builder"]

        self.logger.info("Executing AddMemberBoardCommand")

        if self.parameters.get("version") != "v1":
            raise ValueError("Version not found")

        user_id = self.parameters.get("user")
        if not user_id:
            raise ValueError("User not found")

        board_id = self.parameters.get("id")
        if not board_id:
            raise ValueError("Board not found")

        if not self.request:
            raise ValueError("Request not found")

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

            repository_user = cast(
                domain_security.UserRepository,
                self.repository_getter(
                    repository=domain_security.UserRepository, session=session
                ),
            )

            current_request = cast(AddMemberCommandRequest, self.request)

            entity_board = board_services.add_member_to_board(
                user_to_require_change=user_id,
                board_id=board_id,
                new_member=current_request.user_id,
                repository_board=repository_board,
                repository_ownership=repository_ownership,
                repository_user=repository_user,
                logger=self.logger,
            )
            session.commit()

        return command.CommandResponse(
            trace_id=cast(command.CommandRequest, self.request).trace_id,
            payload=entity_board.model_dump(),
        )


class RemoveMemberCommandRequest(command.CommandRequest):
    user_id: str


class RemoveMemberBoardCommand(command.Command):
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
            request_type=RemoveMemberCommandRequest,
        )

    async def execute(self) -> command.CommandResponse:
        self.logger = self._deps["logger"]
        self.repository_getter = cast(
            repository_model.RepositoryGetter, self._deps["repository_getter"]
        )
        self.uow = self._deps["uow"]
        self.filter_builder = self._deps["filter_builder"]

        self.logger.info("Executing RemoveMemberBoardCommand")

        if self.parameters.get("version") != "v1":
            raise ValueError("Version not found")

        user_id = self.parameters.get("user")
        if not user_id:
            raise ValueError("User not found")

        board_id = self.parameters.get("id")
        if not board_id:
            raise ValueError("Board not found")

        if not self.request:
            raise ValueError("Request not found")

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

            current_request = cast(RemoveMemberCommandRequest, self.request)

            entity_board = board_services.remove_member_to_board(
                user_to_require_change=user_id,
                board_id=board_id,
                to_remove_member=current_request.user_id,
                repository_board=repository_board,
                repository_ownership=repository_ownership,
                logger=self.logger,
            )
            session.commit()

        return command.CommandResponse(
            trace_id=cast(command.CommandRequest, self.request).trace_id,
            payload=entity_board.model_dump(),
        )


class UpdateRoleMemberCommandRequest(command.CommandRequest):
    user_id: str
    role: RoleMemberType


class UpdateRoleMemberBoardCommand(command.Command):
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
            request_type=UpdateRoleMemberCommandRequest,
        )

    async def execute(self) -> command.CommandResponse:
        self.logger = self._deps["logger"]
        self.repository_getter = cast(
            repository_model.RepositoryGetter, self._deps["repository_getter"]
        )
        self.uow = self._deps["uow"]
        self.filter_builder = self._deps["filter_builder"]

        self.logger.info("Executing UpdateRoleMemberBoardCommand")

        if self.parameters.get("version") != "v1":
            raise ValueError("Version not found")

        user_id = self.parameters.get("user")
        if not user_id:
            raise ValueError("User not found")

        board_id = self.parameters.get("id")
        if not board_id:
            raise ValueError("Board not found")

        if not self.request:
            raise ValueError("Request not found")

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

            current_request = cast(UpdateRoleMemberCommandRequest, self.request)

            entity_board = board_services.update_role_in_member(
                user_to_require_change=user_id,
                board_id=board_id,
                member_id=current_request.user_id,
                new_role=current_request.role,
                repository_board=repository_board,
                repository_ownership=repository_ownership,
                logger=self.logger,
            )
            session.commit()

        return command.CommandResponse(
            trace_id=cast(command.CommandRequest, self.request).trace_id,
            payload=entity_board.model_dump(),
        )


# Tasks


class ListTaskCommand(command.Command):
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
            raise ValueError("Board not found")

        if not self.request:
            raise ValueError("Request not found")

        with self.uow.session() as session:
            repository_task = cast(
                domain_repository.TaskRepository,
                self.repository_getter(
                    repository=domain_repository.TaskRepository,
                    session=session,
                ),
            )

            entity_board = task_services.paginate_task_of_board(
                board_id=board_id,
                query=cast(command.CommandQueryRequest, self.request),
                repository_task=repository_task,
                filter_builder=self.filter_builder,
            )

        return command.CommandResponse(
            trace_id=cast(command.CommandRequest, self.request).trace_id,
            payload=getattr(entity_board, "model_dump", lambda: {})(),
        )


class CreateTaskCommand(command.Command):
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
            request_type=task_services.CreateTaskCommandRequest,
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
            raise ValueError("Board not found")

        if not self.request:
            raise ValueError("Request not found")

        with self.uow.session() as session:
            repository_task = cast(
                domain_repository.TaskRepository,
                self.repository_getter(
                    repository=domain_repository.TaskRepository,
                    session=session,
                ),
            )
            repository_history = cast(
                domain_repository.TaskHistoryRepository,
                self.repository_getter(
                    repository=domain_repository.TaskHistoryRepository,
                    session=session,
                ),
            )
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

            entity_task = task_services.create_task(
                payload=cast(task_services.CreateTaskCommandRequest, self.request),
                user_id=user_id,
                board_id=board_id,
                repository_task=repository_task,
                repository_task_history=repository_history,
                repository_board=repository_board,
                repository_ownership=repository_ownership,
                logger=self.logger,
            )

            session.commit()

        return command.CommandResponse(
            trace_id=cast(command.CommandRequest, self.request).trace_id,
            payload=getattr(entity_task, "model_dump", lambda: {})(),
        )


class GetByIDTaskCommand(command.Command):
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

        task_id = self.parameters.get("id")
        if not task_id:
            raise ValueError("Task not found")

        if not self.request:
            raise ValueError("Request not found")

        with self.uow.session() as session:
            repository_task = cast(
                domain_repository.TaskRepository,
                self.repository_getter(
                    repository=domain_repository.TaskRepository,
                    session=session,
                ),
            )
            repository_history = cast(
                domain_repository.TaskHistoryRepository,
                self.repository_getter(
                    repository=domain_repository.TaskHistoryRepository,
                    session=session,
                ),
            )

            entity_task = task_services.get_detailed_task_by_id(
                id=task_id,
                repository_task=repository_task,
                repository_task_history=repository_history,
                filter_builder=self.filter_builder,
            )

        return command.CommandResponse(
            trace_id=cast(command.CommandRequest, self.request).trace_id,
            payload=getattr(entity_task, "model_dump", lambda: {})(),
        )
