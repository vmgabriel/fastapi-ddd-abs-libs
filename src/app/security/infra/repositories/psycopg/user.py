from typing import Any

from src.app.security.domain import UserRepository
from src.domain.models import repository
from src.infra.mixin import postgres


class PostgresUserRepository(
    postgres.PostgresGetterListMixin,
    postgres.PostgresGetterMixin,
    postgres.PostgresCreatorMixin,
    postgres.PostgresUpdaterMixin,
    postgres.PostgresDeleterMixin,
    UserRepository,
):
    def __init__(self, *args, **kwargs) -> None:
        kwargs["repository_persistence"] = kwargs["persistency"] = (
            repository.RepositoryPersistence(
                table_name="tbl_user",
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
        super().__init__(*args, **kwargs)

    def serialize(self, data: Any) -> "PostgresUserRepository":
        self._data = None
        return self
