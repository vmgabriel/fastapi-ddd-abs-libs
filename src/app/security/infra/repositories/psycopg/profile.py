from typing import Any

from src.app.security.domain import ProfileRepository
from src.domain.models import repository
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
        kwargs["repository_persistence"] = kwargs["persistency"] = (
            repository.RepositoryPersistence(
                table_name="tbl_profile",
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

    def serialize(self, data: Any) -> repository.RepositoryData | None:
        return None
