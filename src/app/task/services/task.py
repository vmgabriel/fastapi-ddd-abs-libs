from typing import List, cast

from src.app.shared.services import common as common_service
from src.app.task.domain import entity as entity_domain
from src.app.task.domain import repository as domain_repository
from src.domain.models import filter as filter_domain
from src.domain.services import command


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
