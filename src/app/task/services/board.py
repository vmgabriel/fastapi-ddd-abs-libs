import uuid
from typing import cast

from src.app.security import domain as domain_security
from src.app.shared.services import common as common_service
from src.app.shared.services import user as user_service
from src.app.task.domain import entity as entity_domain
from src.app.task.domain import repository as domain_repository
from src.domain.models import filter as filter_domain
from src.domain.models import repository as repository_model
from src.domain.services import command
from src.infra.log import model as log_model


class UpdateBoardCommandRequest(command.CommandRequest):
    name: str
    description: str
    icon_url: str | None = None


class CreateBoardCommandRequest(UpdateBoardCommandRequest):
    id: str | None


def get_board_by_id(
    id: str,
    repository_board: domain_repository.BoardRepository,
    repository_ownership: domain_repository.OwnerShipBoardRepository,
) -> entity_domain.Board | None:
    try:
        board = cast(entity_domain.Board, repository_board.get_by_id(id=id))
        owners = repository_ownership.get_by_board_id(
            board_id=id,
        )
        if not board:
            raise repository_model.RepositoryNotFoundError()
        for ownership in owners:
            board.inject_member(
                member=entity_domain.BoardMember(
                    user_id=ownership.user_id,
                    board_id=ownership.board_id,
                    role=ownership.role,
                )
            )
        return cast(entity_domain.Board | None, board)
    except repository_model.RepositoryNotFoundError:
        return None


def get_myself_board_by_id(
    user_id: str,
    board_id: str,
    repository_board: domain_repository.BoardRepository,
    repository_ownership: domain_repository.OwnerShipBoardRepository,
) -> entity_domain.Board | None:
    board = get_board_by_id(
        id=board_id,
        repository_board=repository_board,
        repository_ownership=repository_ownership,
    )
    if not board or not board.is_member(
        member=entity_domain.BoardMember(
            user_id=user_id, board_id=board_id, role=entity_domain.RoleMemberType.VIEWER
        )
    ):
        raise ValueError("Board not found")

    return board


def paginate_myself_board(
    user_id: str,
    query: command.CommandQueryRequest,
    repository_view_detailed_board: domain_repository.DetailedBoardRepository,
    filter_builder: filter_domain.FilterBuilder,
) -> filter_domain.Paginator:
    return repository_view_detailed_board.filter_by_user_id(
        user_id=user_id,
        criteria=common_service.command_query_to_criteria(query, filter_builder),
    )


def create_board(
    payload: CreateBoardCommandRequest,
    user_id: str,
    repository_board: domain_repository.BoardRepository,
    repository_ownership: domain_repository.OwnerShipBoardRepository,
    logger: log_model.LogAdapter,
) -> entity_domain.Board:
    entity_board_domain = get_board_by_id(
        repository_board=repository_board,
        repository_ownership=repository_ownership,
        id=cast(str, payload.id),
    )
    if entity_board_domain:
        raise ValueError("Board already exists")
    logger.info("Creating Board")

    new_entity_board = entity_domain.Board.create(
        id=str(payload.id),
        name=payload.name,
        description=payload.description,
        user_id=user_id,
        icon_url=payload.icon_url,
    )

    repository_board.create(new=new_entity_board)
    for member in new_entity_board.members:
        repository_ownership.create(
            new=domain_repository.OwnerShipRepositoryData(
                id=str(uuid.uuid4()),
                board_id=new_entity_board.id,
                user_id=member.user_id,
                role=member.role,
            )
        )

    return new_entity_board


def update_board(
    payload: UpdateBoardCommandRequest,
    user_id: str,
    board_id: str,
    repository_board: domain_repository.BoardRepository,
    repository_ownership: domain_repository.OwnerShipBoardRepository,
    logger: log_model.LogAdapter,
) -> entity_domain.Board:
    entity_board_domain = get_board_by_id(
        repository_board=repository_board,
        repository_ownership=repository_ownership,
        id=board_id,
    )
    if not entity_board_domain:
        raise ValueError(f"Board {board_id} not found")
    logger.info("Updating Board")

    entity_board_domain.update(
        member_that_update=entity_domain.BoardMember(
            user_id=user_id, board_id=board_id, role=entity_domain.RoleMemberType.VIEWER
        ),
        name=payload.name,
        description=payload.description,
        icon_url=payload.icon_url,
    )

    repository_board.update(id=board_id, to_update=entity_board_domain)

    return entity_board_domain


def delete_board(
    board_id: str,
    user_id: str,
    repository_board: domain_repository.BoardRepository,
    repository_ownership: domain_repository.OwnerShipBoardRepository,
    logger: log_model.LogAdapter,
) -> entity_domain.Board:
    entity_board_domain = get_board_by_id(
        repository_board=repository_board,
        repository_ownership=repository_ownership,
        id=board_id,
    )

    if not entity_board_domain:
        raise ValueError(f"Board {board_id} not found")
    logger.info("Deleting Board")

    entity_board_domain.delete(user_id=user_id)

    repository_board.delete(id=board_id)

    return entity_board_domain


def add_member_to_board(
    board_id: str,
    user_to_require_change: str,
    new_member: str,
    repository_board: domain_repository.BoardRepository,
    repository_ownership: domain_repository.OwnerShipBoardRepository,
    repository_user: domain_security.UserRepository,
    logger: log_model.LogAdapter,
) -> entity_domain.Board:
    entity_board_domain = get_board_by_id(
        repository_board=repository_board,
        repository_ownership=repository_ownership,
        id=board_id,
    )

    if not entity_board_domain:
        raise ValueError(f"Board {board_id} not found")

    if (
        user_service.find_user_by_id(id=new_member, user_repository=repository_user)
        is None
    ):
        raise ValueError(f"User {new_member} not found")

    logger.info("Add Member to Board")

    entity_board_domain.add_member(
        member=entity_domain.BoardMember(user_id=new_member, board_id=board_id),
        member_that_update=user_to_require_change,
    )

    repository_ownership.create(
        new=domain_repository.OwnerShipRepositoryData(
            id=str(uuid.uuid4()),
            board_id=board_id,
            user_id=new_member,
            role=entity_domain.RoleMemberType.VIEWER,
        )
    )

    return entity_board_domain


def remove_member_to_board(
    board_id: str,
    user_to_require_change: str,
    to_remove_member: str,
    repository_board: domain_repository.BoardRepository,
    repository_ownership: domain_repository.OwnerShipBoardRepository,
    logger: log_model.LogAdapter,
) -> entity_domain.Board:
    entity_board_domain = get_board_by_id(
        repository_board=repository_board,
        repository_ownership=repository_ownership,
        id=board_id,
    )

    if not entity_board_domain:
        raise ValueError(f"Board {board_id} not found")

    logger.info("Remove Member to Board")

    entity_board_domain.remove_member(
        member=entity_domain.BoardMember(user_id=to_remove_member, board_id=board_id),
        member_that_update=user_to_require_change,
    )

    repository_ownership.delete_by_user_id_and_board_id(
        user_id=to_remove_member, board_id=board_id
    )

    return entity_board_domain


def update_role_in_member(
    board_id: str,
    user_to_require_change: str,
    member_id: str,
    new_role: entity_domain.RoleMemberType,
    repository_board: domain_repository.BoardRepository,
    repository_ownership: domain_repository.OwnerShipBoardRepository,
    logger: log_model.LogAdapter,
) -> entity_domain.Board:
    entity_board_domain = get_board_by_id(
        repository_board=repository_board,
        repository_ownership=repository_ownership,
        id=board_id,
    )

    if not entity_board_domain:
        raise ValueError(f"Board {board_id} not found")

    logger.info(f"Update Role {new_role} in Member {member_id} with board {board_id}")

    entity_board_domain.update_role_member(
        member_that_update=user_to_require_change,
        member_id=member_id,
        role=new_role,
    )

    repository_ownership.update_role_by_user_id_and_board_id(
        user_id=member_id, board_id=board_id, to_update=new_role
    )

    return entity_board_domain
