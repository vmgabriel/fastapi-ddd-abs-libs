from typing import Any

from src.app.security.domain import ProfileRepository
from src.infra.mixin import postgres


class PostgresProfileRepository(ProfileRepository, postgres.PostgresCRUDMixin):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def serialize(self, data: Any) -> "PostgresProfileRepository":
        self._data = None
        return self
