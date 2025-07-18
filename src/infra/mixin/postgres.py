import abc
import functools
from typing import Any, Generator, Iterable, List, Tuple, cast

import pydantic

from src.domain.models import filter, mixin, repository
from src.domain.models.repository import RepositoryData

_SELECT_DEFAULT = "SELECT * FROM {} WHERE {};"
_SELECT_COUNT_DEFAULT = "SELECT COUNT(*) FROM {} WHERE {};"
_SELECT_WITH_OFFSET_LIMIT_DEFAULT = "SELECT * FROM {} WHERE {} LIMIT {} OFFSET {};"

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


class PostgresGetterMixin(mixin.GetterMixin, abc.ABC):

    def get_by_id(self, id: str) -> repository.RepositoryData:
        id_filter_declaration = self._equal_id_filter(id)
        response = self._session.atomic_execute(
            query=_SELECT_DEFAULT.format(
                self.repository_persistence.table_name,
                id_filter_declaration.to_definition(),
            ),
            params=(
                (cast(str, id_filter_declaration.get_values()),)
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
    def filter(self, criteria: filter.Criteria) -> filter.Paginator:
        current_filters = " AND ".join(
            current_filter.to_definition() for current_filter in criteria.filters
        )
        script = _SELECT_WITH_OFFSET_LIMIT_DEFAULT.format(
            self.repository_persistence.table_name,
            current_filters,
            criteria.page_quantity,
            criteria.page_number - 1,
        )
        count_script = _SELECT_COUNT_DEFAULT.format(
            self.repository_persistence.table_name,
            current_filters,
        )

        self.logger.info(f"Query [{script}]")
        self.logger.info(f"Count Query [{count_script}]")

        inject: List[str] = []
        for current_filter in criteria.filters:
            if isinstance(current_filter, filter.FilterDefinition):
                raise NotImplementedError("Filter definitions not implemented")
            curr_filter = current_filter.get_values()
            if isinstance(curr_filter, list):
                inject += cast(Iterable[str], flatten(curr_filter))
                continue
            inject += cast(str, flatten(curr_filter))
        response_count = self._session.atomic_execute(
            query=count_script, params=tuple(inject)
        )

        count = getattr(response_count, "fetchone", lambda: [None])()

        response = self._session.atomic_execute(query=script, params=tuple(inject))

        elements = cast(List[Any], getattr(response, "fetchall", lambda: [])())

        return filter.Paginator(
            total=int(count[0] or 0),
            page=criteria.page_number,
            count=criteria.page_quantity,
            elements=[
                cast(RepositoryData, self.serialize(record)) for record in elements
            ],
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
                "is_active = ?",
                id_filter_declaration.to_definition(),
            ),
            params=("false", cast(str, id_filter_declaration.get_values())),
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
