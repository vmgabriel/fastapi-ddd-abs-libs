from typing import Any, Tuple, cast

from src.app.security.domain import ProfileData, ProfileRepository
from src.domain.models import repository
from src.infra.filter import postgres as filter_postgres
from src.infra.mixin import postgres


class PostgresProfileRepository(
    postgres.PostgresGetterListMixin,
    postgres.PostgresGetterMixin,
    postgres.PostgresCreatorMixin,
    postgres.PostgresUpdaterMixin,
    postgres.PostgresDeleterMixin,
    ProfileRepository,
):
    def __init__(self, *args, **kwargs) -> None:
        self.table_name = "tbl_profile"
        kwargs["repository_persistence"] = kwargs["persistency"] = (
            repository.RepositoryPersistence(
                table_name=self.table_name,
                fields=[
                    "id",
                    "user_id",
                    "phone",
                    "icon_url",
                    "created_at",
                    "updated_at",
                    "deleted_at",
                    "is_activated",
                ],
            )
        )
        super().__init__(*args, **kwargs)

    def by_user_id(self, user_id: str) -> ProfileData | None:
        script = "SELECT * FROM {table} WHERE {filters};"
        _IS_USER_ID_FILTER = filter_postgres.EqualPostgresDefinitionFilter("user_id")
        used_filter = _IS_USER_ID_FILTER(user_id)

        complete_script = script.format(
            table=self.table_name, filters=used_filter.to_definition()
        )
        res = self._session.atomic_execute(
            complete_script,
            (
                (cast(str, used_filter.get_values()),)
                if isinstance(used_filter.get_values(), str)
                else cast(Tuple[str, ...], used_filter.get_values())
            ),
        )

        found = getattr(res, "fetchone", lambda: None)()

        if not found:
            return None

        return self.serialize(found)

    def serialize(self, data: Any) -> ProfileData | None:
        if not data:
            return None
        return ProfileData(
            id=data[0],
            phone=data[1],
            icon_url=data[2],
            is_activated=data[3],
            user_id=data[4],
            created_at=data[5],
            updated_at=data[6],
            deleted_at=data[7],
        )
