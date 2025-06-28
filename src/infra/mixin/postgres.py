import abc
from typing import Generator, Iterable, List, cast

from src.domain.models import filter, mixin, repository

_SELECT_DEFAULT = "SELECT * FROM {} WHERE {};"
_SELECT_COUNT_DEFAULT = "SELECT COUNT(*) FROM {};"
_SELECT_WITH_OFFSET_LIMIT_DEFAULT = "SELECT * FROM {} WHERE {} LIMIT {},{};"

_INSERT_DEFAULT = "INSERT INTO {} ({}) VALUES ({}) RETURNING id;"
_UPDATE_DEFAULT = "UPDATE {} SET {} WHERE {};"
_DELETE_DEFAULT = "UPDATE {} SET {} WHERE {};"


def flatten(items: Iterable | str | bytes) -> Generator[str | bytes, str | bytes, None]:
    if isinstance(items, (str | bytes)):
        yield items
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
            params=tuple(id_filter_declaration.get_values()),
        )
        found = getattr(response, "fetchone", lambda: None)()
        if not found:
            raise repository.RepositoryNotFoundError(
                f"Get_by_id - {self.repository_persistence.table_name} "
                f"not found record with id {id}"
            )
        return self.serialize(found)


class PostgresGetterListMixin(mixin.GetterListMixin, abc.ABC):
    def filter(self, criteria: filter.Criteria) -> filter.Paginator:
        script = _SELECT_WITH_OFFSET_LIMIT_DEFAULT.format(
            self.repository_persistence.table_name,
            " AND ".join(
                current_filter.to_definition() for current_filter in criteria.filters
            ),
            criteria.page_number,
            criteria.page_quantity,
        )
        count_script = _SELECT_COUNT_DEFAULT.format(
            self.repository_persistence.table_name,
        )
        inject: List[str] = []
        for current_filter in criteria.filters:
            if isinstance(current_filter, filter.FilterDefinition):
                raise NotImplementedError("Filter definitions not implemented")
            curr_filter = current_filter.get_values()
            if isinstance(curr_filter, list):
                inject += cast(Iterable[str], flatten(curr_filter))
                continue
            inject += flatten(curr_filter)
        response = self._session.atomic_execute(query=script, params=tuple(inject))
        response_count = self._session.atomic_execute(query=count_script)

        count = getattr(response_count, "fetchone", lambda: None)()

        return filter.Paginator(
            total=int(count or 0),
            page=criteria.page_number,
            count=criteria.page_quantity,
            elements=[
                self.serialize(record)
                for record in getattr(response, "fetchall", lambda: [])()
            ],
        )


class PostgresCreatorMixin(mixin.CreatorMixin):
    def create(self, new: repository.RepositoryData) -> repository.RepositoryData:
        script = _INSERT_DEFAULT.format(
            self.repository_persistence.table_name,
            ",".join(self.repository_persistence.fields),
            ",".join(["%s" for _ in self.repository_persistence.fields]),
        )
        fields = tuple(
            getattr(new, field) for field in self.repository_persistence.fields
        )
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
