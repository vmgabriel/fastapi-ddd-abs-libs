import datetime
from typing import Any, List, cast

from src.app.task.domain import entity as entity_domain
from src.app.task.domain import repository as domain_repository
from src.app.task.domain import views as domain_views
from src.domain.models import filter as filter_domain
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
        self.foreign_key_table_name = "tbl_ownership_board"
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

    def filter_by_user_id(
        self,
        user_id: str,
        criteria: filter_domain.Criteria,
    ) -> filter_domain.Paginator:
        filter_builder_eq = self._filter_builder.build(
            type_filter=filter_domain.FilterType.EQUAL
        )
        user_id_filter = filter_builder_eq("user_id")(user_id)
        user_id_filter.update_table(self.foreign_key_table_name)

        criteria.update_table(self.table_name)
        criteria.append(user_id_filter)

        join = filter_domain.Join(
            join_type=filter_domain.JoinType.INNER,
            on="tbl_ownership_board.board_id = tbl_board.id",
            table=self.foreign_key_table_name,
        )

        board = self.filter(criteria=criteria, joins=[join])

        return board

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
                    "role",
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
            type_filter=filter_domain.FilterType.EQUAL
        )
        order_filter_builder_asc = self._filter_builder.build_order(
            type_order=filter_domain.OrderType.ASC
        )

        criteria_filter = filter_domain.Criteria(
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
            type_filter=filter_domain.FilterType.EQUAL
        )
        order_filter_builder_asc = self._filter_builder.build_order(
            type_order=filter_domain.OrderType.ASC
        )

        criteria_filter = filter_domain.Criteria(
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

    def delete_by_user_id_and_board_id(self, user_id: str, board_id: str) -> None:
        filter_builder_eq = self._filter_builder.build(
            type_filter=filter_domain.FilterType.EQUAL
        )

        order_filter_builder_asc = self._filter_builder.build_order(
            type_order=filter_domain.OrderType.ASC
        )

        criteria_filter = filter_domain.Criteria(
            filters=[
                filter_builder_eq("user_id")(user_id),
                filter_builder_eq("board_id")(board_id),
                filter_builder_eq("is_activated")(True),
            ],
            page_number=1,
            page_quantity=200,
            order_by=[order_filter_builder_asc("id")],
        )

        response_filter = self.filter(criteria=criteria_filter)
        if response_filter.total == 0:
            return None

        response_filter.elements[0].is_activated = False
        response_filter.elements[0].deleted_at = datetime.datetime.now()

        self.update(
            id=response_filter.elements[0].id, to_update=response_filter.elements[0]
        )
        return None

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
            role=data[7],
        )


# Detailed Board

_DETAILED_BOARD_QUERY = """
WITH
user_accessible_boards AS (
        SELECT DISTINCT board_id
        FROM tbl_ownership_board
        WHERE user_id = %s AND tbl_ownership_board.is_activated = TRUE
        {limits}
),
task_status_counts AS (
        SELECT t.board_id,
               t.status,
               COUNT(*) as status_count
        FROM user_accessible_boards uab
            JOIN tbl_board b ON b.id = uab.board_id
            JOIN tbl_task t ON t.board_id = b.id
        WHERE t.status IS NOT NULL
        GROUP BY t.board_id, t.status
),
board_task_metrics AS MATERIALIZED (
    SELECT
        b.id as board_id,
        COUNT(t.*) as total_count,
        SUM(CASE WHEN t.is_activated THEN 1 ELSE 0 END) as active_count,
        SUM(CASE WHEN NOT t.is_activated THEN 1 ELSE 0 END) as inactive_count,
        (
            SELECT jsonb_object_agg(status, status_count)
            FROM task_status_counts tsc
            WHERE tsc.board_id = b.id
        ) as status_distribution
    FROM user_accessible_boards uab
        JOIN tbl_board b ON b.id = uab.board_id
        LEFT JOIN tbl_task t ON t.board_id = b.id
    GROUP BY b.id
),
board_member_details AS (
    SELECT
        ob.board_id,
        jsonb_agg(jsonb_build_object(
                'user_id', u.id,
                'full_name', concat(u.name, ' ', u.last_name),
                'username', u.username,
                'contact', jsonb_build_object(
                        'email', u.email,
                        'phone', p.phone
                ),
                'profile_id', p.id,
                'icon_url', p.icon_url,
                'role', ob.role
        )) as members
    FROM user_accessible_boards uab
        JOIN tbl_ownership_board ob ON ob.board_id = uab.board_id
        JOIN tbl_user u ON ob.user_id = u.id
        JOIN tbl_profile p ON u.id = p.user_id
    GROUP BY ob.board_id
)
SELECT
    {attributes}
FROM {table} b
    {joins}
    JOIN user_accessible_boards uab ON b.id = uab.board_id
    LEFT JOIN board_member_details bm ON b.id = bm.board_id
    LEFT JOIN board_task_metrics btm ON b.id = btm.board_id
{filters}
;
"""

_ATTRIBUTES_DETAILED = """
,
COALESCE(bm.members, '[]'::jsonb) as members,
COALESCE(btm.total_count, 0) as total_tasks,
    COALESCE(btm.active_count, 0) as active_tasks,
    COALESCE(btm.inactive_count, 0) as inactive_tasks,
    COALESCE(btm.status_distribution, '{}'::jsonb) as task_status_summary
"""


class PostgresDetailedBoardRepository(
    postgres.PostgresGetterMixin,
    postgres.PostgresGetterListMixin,
    domain_repository.DetailedBoardRepository,
):
    custom_query: repository.CustomQuery

    def __init__(self, *args, **kwargs) -> None:
        self.table_name = "tbl_board"
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

        self.custom_query = postgres.PostgresCustomQuery(query=_DETAILED_BOARD_QUERY)

    def filter_by_user_id(
        self, user_id: str, criteria: filter_domain.Criteria
    ) -> filter_domain.Paginator:
        criteria.update_table("b")
        criteria.append(
            self._filter_builder.build(type_filter=filter_domain.FilterType.EQUAL)(
                "b.is_activated"
            )(True)
        )

        current_filters = self._create_filters(filters=criteria.filters)
        if current_filters:
            current_filters = "WHERE " + current_filters
        else:
            current_filters = ""
        current_joins = ""

        script = self.custom_query.query.format(
            "{}",
            table=self.repository_persistence.table_name,
            attributes="b.*" + _ATTRIBUTES_DETAILED,
            joins=current_joins,
            filters=current_filters,
            limits="LIMIT {limit} OFFSET {offset}".format(
                limit=str(criteria.page_quantity or 30),
                offset=str((criteria.page_number or 1) - 1),
            ),
        )
        count_script = self.custom_query.query.format(
            "{}",
            table=self.repository_persistence.table_name,
            attributes="count(b.*)",
            joins=current_joins,
            filters=current_filters,
            limits="",
        )

        self.logger.info(f"Query [{script}]")
        self.logger.info(f"Count Query [{count_script}]")

        filter_for_user_id = self._filter_builder.build(
            type_filter=filter_domain.FilterType.EQUAL
        )("tbl_ownership_board.user_id")(user_id)

        inject = self._create_params_filter(
            filters=criteria.filters, pre_filters=[filter_for_user_id]
        )

        response_count = self._session.atomic_execute(query=count_script, params=inject)
        count = getattr(response_count, "fetchone", lambda: [None])()

        response = self._session.atomic_execute(query=script, params=inject)
        elements = cast(List[Any], getattr(response, "fetchall", lambda: [])())

        total = int(count[0] or 0)

        return filter_domain.Paginator(
            total=total,
            page=criteria.page_number or 1,
            count=(
                (criteria.page_quantity or 1)
                if total > (criteria.page_quantity or 1)
                else total
            ),
            elements=[self.serialize(record) for record in elements],
        )

    def serialize(self, data: Any) -> domain_views.DetailedBoard | None:
        if not data:
            return None

        task_summary = domain_views.BoardTaskSummary(
            total=data[9],
            active=data[10],
            inactive=data[11],
            summary_status=data[12],
        )

        return domain_views.DetailedBoard(
            id=data[0],
            name=data[1],
            description=data[2],
            icon_url=data[3],
            is_activated=data[4],
            created_at=data[5],
            updated_at=data[6],
            deleted_at=data[7],
            task_summary=task_summary,
            members=[
                domain_views.BoardMember.model_validate(member) for member in data[8]
            ],
        )
