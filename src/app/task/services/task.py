from typing import List, cast

from src.app.shared.services import common as common_service
from src.app.task.domain import entity as entity_domain
from src.app.task.domain import repository as domain_repository
from src.domain.models import filter as filter_domain
from src.domain.models import repository as repository_model
from src.domain.services import command
from src.infra.log import model as log_model

from . import board as services_board


def get_histories_by_task_id(
    task_id: str,
    repository_task_history: domain_repository.TaskHistoryRepository,
) -> List[entity_domain.TaskHistory]:
    return repository_task_history.get_by_task_id(task_id=task_id)


def get_task_by_id(
    id: str,
    repository_task: domain_repository.TaskRepository,
    repository_task_history: domain_repository.TaskHistoryRepository,
) -> entity_domain.Task | None:
    try:
        task = cast(entity_domain.Task, repository_task.get_by_id(id=id))
        histories = get_histories_by_task_id(
            task_id=id, repository_task_history=repository_task_history
        )
        if not task:
            raise repository_model.RepositoryNotFoundError(
                f"Not Found Task With ID {id}"
            )
        for history in histories:
            task.inject_history(history=history)
        return cast(entity_domain.Task | None, task)
    except repository_model.RepositoryNotFoundError:
        return None


def paginate_task_of_board(
    board_id: str,
    query: command.CommandQueryRequest,
    repository_task: domain_repository.TaskRepository,
    filter_builder: filter_domain.FilterBuilder,
) -> filter_domain.Paginator:
    eq_filter = filter_builder.build(type_filter=filter_domain.FilterType.EQUAL)
    no_eq_filter = filter_builder.build(type_filter=filter_domain.FilterType.NOT_EQUAL)

    board_id_eq_filter = eq_filter("board_id")(board_id)
    is_activated_eq_filter = eq_filter("is_activated")(True)
    status_not_eq_filter = no_eq_filter("status")(entity_domain.TaskStatus.ABANDONED)

    criteria_task = common_service.command_query_to_criteria(query, filter_builder)

    criteria_task.append(board_id_eq_filter)
    criteria_task.append(is_activated_eq_filter)
    criteria_task.append(status_not_eq_filter)

    for filter in cast(List[filter_domain.Filter], criteria_task.filters):
        filter.update_table("tbl_task")

    join_with_user = filter_domain.Join(
        table="tbl_user",
        on="tbl_task.user_id = tbl_user.id",
        join_type=filter_domain.JoinType.INNER,
    )
    join_user_with_profile = filter_domain.Join(
        table="tbl_profile",
        on="tbl_user.id = tbl_profile.user_id",
        join_type=filter_domain.JoinType.INNER,
    )

    return repository_task.filter(
        criteria=criteria_task, joins=[join_with_user, join_user_with_profile]
    )


def get_detailed_task_by_id(
    id: str,
    repository_task: domain_repository.TaskRepository,
    repository_task_history: domain_repository.TaskHistoryRepository,
    filter_builder: filter_domain.FilterBuilder,
) -> entity_domain.Task | None:
    eq_filter = filter_builder.build(type_filter=filter_domain.FilterType.EQUAL)
    order_by_id = filter_builder.build_order(type_order=filter_domain.OrderType.ASC)(
        "id"
    )

    user_id_eq_filter = eq_filter("id")(id)
    is_activated_eq_filter = eq_filter("is_activated")(True)

    criteria_task = filter_domain.Criteria(
        filters=[user_id_eq_filter, is_activated_eq_filter],
        order_by=[order_by_id],
        page_quantity=30,
        page_number=1,
    )

    for filter in cast(List[filter_domain.Filter], criteria_task.filters):
        filter.update_table("tbl_task")

    join_with_user = filter_domain.Join(
        table="tbl_user",
        on="tbl_task.user_id = tbl_user.id",
        join_type=filter_domain.JoinType.INNER,
    )
    join_user_with_profile = filter_domain.Join(
        table="tbl_profile",
        on="tbl_user.id = tbl_profile.user_id",
        join_type=filter_domain.JoinType.INNER,
    )

    task_paginator = repository_task.filter(
        criteria=criteria_task, joins=[join_with_user, join_user_with_profile]
    )

    if task_paginator.total == 0:
        raise ValueError("Task not found")

    task = task_paginator.elements[0]
    histories = get_histories_by_task_id(
        task_id=id, repository_task_history=repository_task_history
    )
    for history in histories:
        task.inject_history(history=history)
    return cast(entity_domain.Task | None, task)


class UpdateTaskCommandRequest(command.CommandRequest):
    name: str
    description: str
    priority: entity_domain.PriorityType
    icon_url: str | None = None


class CreateTaskCommandRequest(UpdateTaskCommandRequest):
    id: str | None


def create_task(
    payload: CreateTaskCommandRequest,
    user_id: str,
    board_id: str,
    logger: log_model.LogAdapter,
    repository_task: domain_repository.TaskRepository,
    repository_task_history: domain_repository.TaskHistoryRepository,
    repository_board: domain_repository.BoardRepository,
    repository_ownership: domain_repository.OwnerShipBoardRepository,
) -> entity_domain.Task:
    entity_task_domain = get_task_by_id(
        repository_task=repository_task,
        repository_task_history=repository_task_history,
        id=cast(str, payload.id),
    )
    if entity_task_domain:
        raise ValueError("Task already exists")

    entity_board_domain = services_board.get_board_by_id(
        id=board_id,
        repository_board=repository_board,
        repository_ownership=repository_ownership,
    )
    if not entity_board_domain:
        raise ValueError("Board not found")

    logger.info("Creating Task")

    new_entity_task = entity_domain.Task.create(
        id=str(payload.id),
        name=payload.name,
        description=payload.description,
        owner=user_id,
        board_id=board_id,
        priority=payload.priority,
        icon_url=payload.icon_url,
    )
    entity_board_domain.add_task(task=new_entity_task, member_that_insert=user_id)

    repository_task.create(new=new_entity_task)
    repository_task_history.create(new=new_entity_task.histories[0])
    return new_entity_task


def update_task(
    id: str,
    user_id: str,
    payload: UpdateTaskCommandRequest,
    logger: log_model.LogAdapter,
    repository_task: domain_repository.TaskRepository,
    repository_task_history: domain_repository.TaskHistoryRepository,
    repository_board: domain_repository.BoardRepository,
    repository_ownership: domain_repository.OwnerShipBoardRepository,
) -> entity_domain.Task:
    entity_task_domain = get_task_by_id(
        repository_task=repository_task,
        repository_task_history=repository_task_history,
        id=id,
    )

    if not entity_task_domain:
        raise ValueError("Task not found")

    entity_board_domain = services_board.get_board_by_id(
        id=entity_task_domain.board_id,
        repository_board=repository_board,
        repository_ownership=repository_ownership,
    )
    if not entity_board_domain:
        raise ValueError("Board not found")

    logger.info("Updating Task")

    entity_task_domain.update(
        name=payload.name,
        description=payload.description,
        priority=payload.priority,
        icon_url=payload.icon_url,
    )
    entity_board_domain.update_task(task=entity_task_domain, member_that_update=user_id)

    repository_task.update(id=id, to_update=entity_task_domain)
    repository_task_history.create(new=entity_task_domain.histories[-1])
    return entity_task_domain


def delete_task(
    id: str,
    user_id: str,
    logger: log_model.LogAdapter,
    repository_task: domain_repository.TaskRepository,
    repository_task_history: domain_repository.TaskHistoryRepository,
    repository_board: domain_repository.BoardRepository,
    repository_ownership: domain_repository.OwnerShipBoardRepository,
) -> entity_domain.Task:
    entity_task_domain = get_task_by_id(
        repository_task=repository_task,
        repository_task_history=repository_task_history,
        id=id,
    )

    if not entity_task_domain:
        raise ValueError("Task not found")

    entity_board_domain = services_board.get_board_by_id(
        id=entity_task_domain.board_id,
        repository_board=repository_board,
        repository_ownership=repository_ownership,
    )
    if not entity_board_domain:
        raise ValueError("Board not found")

    logger.info("Deleting Task")

    entity_task_domain.delete()
    entity_board_domain.delete_task(task=entity_task_domain, member_that_delete=user_id)

    repository_task.delete(id=id)
    repository_task_history.create(new=entity_task_domain.histories[-1])
    return entity_task_domain
