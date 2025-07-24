from typing import Any, List, cast

from src.app.task.domain import entity as entity_domain
from src.app.task.domain import repository as domain_repository
from src.domain.models import filter as filter_domain
from src.domain.models import repository
from src.infra.mixin import postgres


class PostgresTaskRepository(
    postgres.PostgresGetterListMixin,
    postgres.PostgresGetterMixin,
    postgres.PostgresCreatorMixin,
    postgres.PostgresUpdaterMixin,
    postgres.PostgresDeleterMixin,
    domain_repository.TaskRepository,
):
    def __init__(self, *args, **kwargs) -> None:
        self.table_name = "tbl_task"
        kwargs["repository_persistence"] = kwargs["persistency"] = (
            repository.RepositoryPersistence(
                table_name=self.table_name,
                fields=[
                    "id",
                    "board_id",
                    "name",
                    "description",
                    "user_id",
                    "status",
                    "icon_url",
                    "priority",
                    "created_at",
                    "updated_at",
                    "deleted_at",
                    "is_activated",
                ],
            )
        )
        super().__init__(*args, **kwargs)

    def serialize(self, data: Any) -> entity_domain.Task | None:
        if not data:
            return None

        owner_data = {}
        if len(data) > 12:
            owner_data = {
                "user_id": data[12],
                "username": data[15],
                "icon_id": data[25],
                "full_name": data[13] + " " + data[14],
            }

        return entity_domain.Task(
            id=data[0],
            owner=data[1],
            name=data[2],
            description=data[3],
            status=data[4],
            icon_url=data[5],
            is_activated=data[6],
            created_at=data[7],
            updated_at=data[8],
            deleted_at=data[9],
            board_id=data[10],
            priority=entity_domain.PriorityType(data[11]),
            owner_data=owner_data,
        )


class PostgresHistoryTaskRepository(
    postgres.PostgresGetterListMixin,
    postgres.PostgresGetterMixin,
    postgres.PostgresCreatorMixin,
    postgres.PostgresUpdaterMixin,
    postgres.PostgresDeleterMixin,
    domain_repository.TaskHistoryRepository,
):
    def __init__(self, *args, **kwargs) -> None:
        self.table_name = "tbl_history_task"
        kwargs["repository_persistence"] = kwargs["persistency"] = (
            repository.RepositoryPersistence(
                table_name=self.table_name,
                fields=[
                    "id",
                    "task_id",
                    "changed_at",
                    "type_of_change",
                    "previous_values",
                    "new_values",
                    "created_at",
                    "updated_at",
                    "deleted_at",
                    "is_activated",
                ],
            )
        )
        super().__init__(*args, **kwargs)

    def get_by_task_id(self, task_id: str) -> List[entity_domain.TaskHistory]:
        filter_builder_eq = self._filter_builder.build(
            type_filter=filter_domain.FilterType.EQUAL
        )
        order_filter_builder_asc = self._filter_builder.build_order(
            type_order=filter_domain.OrderType.ASC
        )

        criteria_filter = filter_domain.Criteria(
            filters=[
                filter_builder_eq("task_id")(task_id),
                filter_builder_eq("is_activated")(True),
            ],
            page_number=1,
            page_quantity=200,
            order_by=[order_filter_builder_asc("id")],
        )

        response_filter = self.filter(criteria=criteria_filter)

        return cast(List[entity_domain.TaskHistory], response_filter.elements)

    def serialize(self, data: Any) -> entity_domain.TaskHistory | None:
        if not data:
            return None
        return entity_domain.TaskHistory(
            id=data[0],
            task_id=data[1],
            changed_at=data[2],
            type_of_change=data[3],
            previous_values=data[4],
            new_values=data[5],
            is_activated=data[6],
            created_at=data[7],
            updated_at=data[8],
            deleted_at=data[9],
        )
