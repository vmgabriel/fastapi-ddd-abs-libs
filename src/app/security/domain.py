import abc
from typing import Any, Dict

from src.domain.models import mixin, repository
from src.domain.services import user


class ProfileData(repository.RepositoryData, user.AuthUser):
    email: str


class ProfileRepository(repository.Repository, mixin.CRUDMixin, abc.ABC):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def dict(self) -> Dict[str, Any]:
        if not self._data:
            return {}
        return self._data.model_dump()
