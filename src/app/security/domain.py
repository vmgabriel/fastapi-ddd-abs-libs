import abc
from typing import Any, Dict

from src.domain.models import mixin, repository
from src.domain.services import user


class UserData(repository.RepositoryData, user.AuthUser):
    email: str
    password: str
    permissions: list[str]


class ProfileData(repository.RepositoryData):
    user_id: str
    phone: str | None = None
    icon_url: str | None = None


class ProfileRepository(
    repository.Repository,
    mixin.GetterMixin,
    mixin.GetterListMixin,
    mixin.CreatorMixin,
    mixin.UpdaterMixin,
    mixin.DeleterMixin,
    abc.ABC,
):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def dict(self) -> Dict[str, Any]:
        if not self._data:
            return {}
        return self._data.model_dump()


class UserRepository(
    repository.Repository,
    mixin.GetterMixin,
    mixin.GetterListMixin,
    mixin.CreatorMixin,
    mixin.UpdaterMixin,
    mixin.DeleterMixin,
    abc.ABC,
):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def dict(self) -> Dict[str, Any]:
        if not self._data:
            return {}
        return self._data.model_dump()
