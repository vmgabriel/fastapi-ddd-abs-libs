from typing import Any, Tuple, cast

from src.app.security import domain as security_domain
from src.domain.models import repository
from src.infra.filter import postgres as filter_postgres
from src.infra.mixin import postgres


class PostgresUserRepository(
    postgres.PostgresGetterListMixin,
    postgres.PostgresGetterMixin,
    postgres.PostgresCreatorMixin,
    postgres.PostgresUpdaterMixin,
    postgres.PostgresDeleterMixin,
    security_domain.UserRepository,
):
    def __init__(self, *args, **kwargs) -> None:
        self.table_name = "tbl_user"
        kwargs["repository_persistence"] = kwargs["persistency"] = (
            repository.RepositoryPersistence(
                table_name=self.table_name,
                fields=[
                    "id",
                    "name",
                    "last_name",
                    "username",
                    "email",
                    "password",
                    "permissions",
                    "created_at",
                    "updated_at",
                    "deleted_at",
                    "is_activated",
                ],
            )
        )
        self.script = "SELECT * FROM {table} WHERE {filters};"

        super().__init__(*args, **kwargs)

    def by_username(self, username: str) -> security_domain.UserData | None:
        _IS_USERNAME_FILTER = filter_postgres.EqualPostgresDefinitionFilter("username")
        used_filter = _IS_USERNAME_FILTER(username)

        complete_script = self.script.format(
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

    def by_email(self, email: str) -> security_domain.UserData | None:
        _IS_EMAIL_FILTER = filter_postgres.EqualPostgresDefinitionFilter("email")
        used_filter = _IS_EMAIL_FILTER(email)

        complete_script = self.script.format(
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

    def serialize(self, data: Any) -> security_domain.UserData | None:
        return security_domain.UserData(
            id=data[0],
            name=data[1],
            last_name=data[2],
            username=data[3],
            email=data[4],
            is_activated=data[5],
            created_at=data[6],
            updated_at=data[7],
            deleted_at=data[8],
            permissions=cast(str, data[9]).split(","),
            password=data[10],
        )
