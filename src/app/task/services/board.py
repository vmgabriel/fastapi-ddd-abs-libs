import uuid
from typing import cast

from src.app.task.domain import entity as entity_domain
from src.app.task.domain import repository as domain_repository
from src.domain.models import repository as repository_model
from src.domain.services import command
from src.infra.log import model as log_model


class CreateBoardCommandRequest(command.CommandRequest):
    name: str
    description: str
    id: str | None
    icon_url: str | None = None


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
            board.add_owner(user_id=ownership.user_id)
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
    if not board or not board.is_owner(user_id=user_id):
        raise ValueError("Board not found")

    return board


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
    for owner in new_entity_board.owners:
        repository_ownership.create(
            new=domain_repository.OwnerShipRepositoryData(
                id=str(uuid.uuid4()),
                board_id=new_entity_board.id,
                user_id=owner,
            )
        )

    return new_entity_board
