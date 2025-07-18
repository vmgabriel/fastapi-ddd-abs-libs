from typing import Any

from src.app.task.domain import entity as entity_domain
from src.app.task.domain import repository as domain_repository
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
                    "user_id",
                    "name",
                    "description",
                    "status",
                    "icon_url",
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
        return entity_domain.Task(
            id=data[0],
            owner=data[1],
            name=data[2],
            description=data[3],
            status=data[4],
            icon_url=data[5],
            created_at=data[6],
            updated_at=data[7],
            deleted_at=data[8],
            is_activated=data[9],
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
            created_at=data[6],
            updated_at=data[7],
            deleted_at=data[8],
            is_activated=data[9],
        )
