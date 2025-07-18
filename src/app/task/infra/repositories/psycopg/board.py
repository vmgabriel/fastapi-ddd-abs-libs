from typing import Any, List, cast

from src.app.task.domain import entity as entity_domain
from src.app.task.domain import repository as domain_repository
from src.domain.models import filter, repository
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

    def get_by_user_id_and_board_id(
        self, user_id: str, board_id: str
    ) -> domain_repository.OwnerShipRepositoryData | None:
        filter_builder_eq = self._filter_builder.build(
            type_filter=filter.FilterType.EQUAL
        )
        order_filter_builder_asc = self._filter_builder.build_order(
            type_order=filter.OrderType.ASC
        )

        criteria_filter = filter.Criteria(
            filters=[
                filter_builder_eq("user_id")(user_id),
                filter_builder_eq("board_id")(board_id),
            ],
            page_number=1,
            page_quantity=1,
            order_by=[order_filter_builder_asc("id")],
        )

        response_filter = self.filter(criteria=criteria_filter)

        if response_filter.total == 0:
            return None

        return cast(
            domain_repository.OwnerShipRepositoryData, response_filter.elements[0]
        )

    def get_by_board_id(
        self, board_id: str
    ) -> List[domain_repository.OwnerShipRepositoryData]:
        filter_builder_eq = self._filter_builder.build(
            type_filter=filter.FilterType.EQUAL
        )
        order_filter_builder_asc = self._filter_builder.build_order(
            type_order=filter.OrderType.ASC
        )

        criteria_filter = filter.Criteria(
            filters=[
                filter_builder_eq("board_id")(board_id),
            ],
            page_number=1,
            page_quantity=200,
            order_by=[order_filter_builder_asc("id")],
        )

        response_filter = self.filter(criteria=criteria_filter)

        return cast(
            List[domain_repository.OwnerShipRepositoryData], response_filter.elements
        )

    def serialize(self, data: Any) -> domain_repository.OwnerShipRepositoryData | None:
        if not data:
            return None
        return domain_repository.OwnerShipRepositoryData(
            id=data[0],
            board_id=data[1],
            user_id=data[2],
            is_activated=data[3],
            created_at=data[4],
            updated_at=data[5],
            deleted_at=data[6],
        )
