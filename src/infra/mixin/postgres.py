import abc
import datetime
import functools
from typing import Any, Generator, Iterable, List, Tuple, cast

import pydantic

from src.domain.models import filter, mixin, repository
from src.domain.models.repository import RepositoryData

_SELECT_DEFAULT = "SELECT * FROM {} WHERE {};"
_SELECT_WITH_OFFSET_LIMIT_DEFAULT = (
    "SELECT {attributes} FROM {table} {joins} WHERE {filters} {limits};"
)

_INSERT_DEFAULT = "INSERT INTO {} ({}) VALUES ({}) RETURNING id;"
_UPDATE_DEFAULT = "UPDATE {} SET {} WHERE {};"
_DELETE_DEFAULT = "UPDATE {} SET {} WHERE {};"


def flatten(items: Iterable | str | bytes) -> Generator[str | bytes, str | bytes, None]:
    if isinstance(items, (str, bytes)):
        yield items
        return
    for item in items:
        if isinstance(item, Iterable):
            yield from flatten(item)
        else:
            yield cast(str | bytes, item)


class PostgresCustomQuery(repository.CustomQuery):
    def __init__(self, query: str) -> None:
        super().__init__(
            query=query,
            count_attributes="COUNT(*)",
            limit_offset="LIMIT {limit} OFFSET {offset}",
        )


DEFAULT_CUSTOM_QUERY = PostgresCustomQuery(query=_SELECT_WITH_OFFSET_LIMIT_DEFAULT)


class PostgresGetterMixin(mixin.GetterMixin, abc.ABC):

    def get_by_id(self, id: str) -> repository.RepositoryData:
        id_filter_declaration = self._equal_id_filter(id)
        just_activated_filter = self._filter_builder.build(
            type_filter=filter.FilterType.EQUAL
        )("is_activated")(True)
        response = self._session.atomic_execute(
            query=_SELECT_DEFAULT.format(
                self.repository_persistence.table_name,
                id_filter_declaration.to_definition()
                + " AND "
                + just_activated_filter.to_definition(),
            ),
            params=(
                (
                    cast(str, id_filter_declaration.get_values()),
                    cast(str, just_activated_filter.get_values()),
                )
                if isinstance(id_filter_declaration.get_values(), str)
                else cast(Tuple[str, ...], id_filter_declaration.get_values())
            ),
        )
        found = getattr(response, "fetchone", lambda: None)()
        if not found:
            raise repository.RepositoryNotFoundError(
                f"Get_by_id - {self.repository_persistence.table_name} "
                f"not found record with id {id}"
            )
        return cast(RepositoryData, self.serialize(found))


class PostgresGetterListMixin(mixin.GetterListMixin, abc.ABC):
    def _create_filters(
        self,
        filters: (
            List[filter.Filter | filter.AndFilters | filter.OrFilters] | None
        ) = None,
    ) -> str:
        current_filters = ""
        if not filters:
            return current_filters

        return " AND ".join(
            current_filter.to_definition() for current_filter in filters
        )

    def _create_joins(self, joins: List[filter.Join] | None = None) -> str:
        current_joins = ""
        if not joins:
            return current_joins

        join_handler = cast(filter.Joined, self._filter_builder.join)

        return " ".join(join_handler.to_definition(join) for join in joins if join)

    def _create_params_filter(
        self,
        pre_filters: (
            List[filter.Filter | filter.AndFilters | filter.OrFilters] | None
        ) = None,
        filters: (
            List[filter.Filter | filter.AndFilters | filter.OrFilters] | None
        ) = None,
    ) -> Tuple[str, ...] | None:
        if not filters:
            filters = []

        if not filters and not pre_filters:
            return None

        inject: List[str] = []

        if pre_filters:
            for pre_filter in pre_filters:
                filters.insert(0, pre_filter)

        for current_filter in filters:
            curr_filter = current_filter.get_values()
            if isinstance(curr_filter, list):
                inject += cast(Iterable[str], flatten(curr_filter))
                continue
            inject += cast(str, flatten(curr_filter))
        return tuple(inject)

    def filter(
        self,
        criteria: filter.Criteria,
        custom_query: repository.CustomQuery | None = None,
        joins: List[filter.Join] | None = None,
    ) -> filter.Paginator:
        if not custom_query:
            custom_query = DEFAULT_CUSTOM_QUERY

        current_filters = self._create_filters(filters=criteria.filters)
        current_joins = self._create_joins(joins)

        script = custom_query.to_declaration(
            table_name=self.repository_persistence.table_name,
            attributes="*",
            joins=current_joins,
            filters=current_filters,
            limit=str(criteria.page_quantity),
            offset=str(criteria.page_number - 1),
        )
        count_script = custom_query.to_declaration(
            with_count=True,
            table_name=self.repository_persistence.table_name,
            attributes=custom_query.count_attributes,
            joins=current_joins,
            filters=current_filters,
            limit=str(criteria.page_quantity),
            offset=str(criteria.page_number - 1),
        )

        self.logger.info(f"Query [{script}]")
        self.logger.info(f"Count Query [{count_script}]")

        inject = self._create_params_filter(filters=criteria.filters)

        response_count = self._session.atomic_execute(query=count_script, params=inject)
        count = getattr(response_count, "fetchone", lambda: [None])()

        response = self._session.atomic_execute(query=script, params=inject)
        elements = cast(List[Any], getattr(response, "fetchall", lambda: [])())

        total = int(count[0] or 0)

        return filter.Paginator(
            total=total,
            page=criteria.page_number,
            count=criteria.page_quantity if total > criteria.page_quantity else total,
            elements=[self.serialize(record) for record in elements],
        )


class PostgresCreatorMixin(mixin.CreatorMixin):
    def create(self, new: repository.RepositoryData) -> repository.RepositoryData:
        script = _INSERT_DEFAULT.format(
            self.repository_persistence.table_name,
            ",".join(self.repository_persistence.fields),
            ",".join(["%s" for _ in self.repository_persistence.fields]),
        )

        def convertion_fields(field: Any) -> str:
            if isinstance(field, pydantic.SecretStr):
                return field.get_secret_value()
            if isinstance(field, list):
                return ",".join(field)
            return field

        get_fields = (
            getattr(new, field) for field in self.repository_persistence.fields
        )
        fields_to_attr = functools.partial(
            map,
            convertion_fields,
        )

        fields = tuple(fields_to_attr(get_fields))
        self.logger.info(f"Query [{script}]")
        result = self._session.atomic_execute(query=script, params=fields)
        new_id = getattr(result, "fetchone", lambda: "")()
        new.id = new_id[0] if new_id else ""
        return new


class PostgresUpdaterMixin(mixin.UpdaterMixin):
    def update(
        self, id: str, to_update: repository.RepositoryData
    ) -> repository.RepositoryData:
        script = _UPDATE_DEFAULT.format(
            self.repository_persistence.table_name,
            ",".join(
                [
                    f"{field} = %s"
                    for field in self.repository_persistence.fields
                    if field != "id"
                ]
            ),
            "id = %s",
        )
        self._session.atomic_execute(
            query=script,
            params=(
                *(
                    getattr(to_update, field)
                    for field in self.repository_persistence.fields
                    if field != "id"
                ),
                id,
            ),
        )
        return to_update


class PostgresDeleterMixin(mixin.DeleterMixin):
    def delete(self, id: str) -> None:
        id_filter_declaration = self._equal_id_filter(id)
        self._session.atomic_execute(
            query=_DELETE_DEFAULT.format(
                self.repository_persistence.table_name,
                "deleted_at = %s, is_activated = %s",
                id_filter_declaration.to_definition(),
            ),
            params=(
                datetime.datetime.now().isoformat(),
                "false",
                cast(str, id_filter_declaration.get_values()),
            ),
        )


class PostgresCRUDMixin(
    mixin.GetterMixin,
    mixin.CreatorMixin,
    mixin.UpdaterMixin,
    mixin.DeleterMixin,
    abc.ABC,
):
    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(
            *args,
            **kwargs,
        )
