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


def create_board(
    payload: CreateBoardCommandRequest,
    user_id: str,
    repository_board: domain_repository.BoardRepository,
    repository_ownership: domain_repository.OwnerShipBoardRepository,
    logger: log_model.LogAdapter,
) -> entity_domain.Board:
    try:
        if repository_board.get_by_id(id=cast(str, payload.id)):
            raise ValueError("Board already exists")
    except repository_model.RepositoryNotFoundError:
        logger.info("Board not found - Creating new one")

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
