from typing import Any

from src.app.task.domain import entity as entity_domain
from src.app.task.domain import repository as domain_repository
from src.domain.models import repository
from src.infra.mixin import postgres


class PostgresBoardRepository(
    postgres.PostgresGetterListMixin,
    postgres.PostgresGetterMixin,
    postgres.PostgresCreatorMixin,
    postgres.PostgresUpdaterMixin,
    postgres.PostgresDeleterMixin,
    domain_repository.BoardRepository,
):
    def __init__(self, *args, **kwargs) -> None:
        self.table_name = "tbl_board"
        kwargs["repository_persistence"] = kwargs["persistency"] = (
            repository.RepositoryPersistence(
                table_name=self.table_name,
                fields=[
                    "id",
                    "name",
                    "description",
                    "icon_url",
                    "created_at",
                    "updated_at",
                    "deleted_at",
                    "is_activated",
                ],
            )
        )
        super().__init__(*args, **kwargs)

    def serialize(self, data: Any) -> entity_domain.Board | None:
        if not data:
            return None
        return entity_domain.Board(
            id=data[0],
            name=data[1],
            description=data[2],
            icon_url=data[3],
        )


class PostgresOwnerShipBoardRepository(
    postgres.PostgresGetterListMixin,
    postgres.PostgresGetterMixin,
    postgres.PostgresCreatorMixin,
    postgres.PostgresUpdaterMixin,
    postgres.PostgresDeleterMixin,
    domain_repository.OwnerShipBoardRepository,
):
    def __init__(self, *args, **kwargs) -> None:
        self.table_name = "tbl_ownership_board"
        kwargs["repository_persistence"] = kwargs["persistency"] = (
            repository.RepositoryPersistence(
                table_name=self.table_name,
                fields=[
                    "id",
                    "board_id",
                    "user_id",
                    "created_at",
                    "updated_at",
                    "deleted_at",
                    "is_activated",
                ],
            )
        )
        super().__init__(*args, **kwargs)

    def serialize(self, data: Any) -> domain_repository.OwnerShipRepositoryData | None:
        if not data:
            return None
        return domain_repository.OwnerShipRepositoryData(
            id=data[0],
            board_id=data[1],
            user_id=data[2],
            created_at=data[3],
            updated_at=data[4],
            deleted_at=data[5],
            is_activated=data[6],
        )
