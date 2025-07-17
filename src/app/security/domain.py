import abc

import pydantic

from src.domain import libtools
from src.domain.models import mixin, repository
from src.domain.services import user


class UserData(repository.RepositoryData, user.AuthUser):
    email: str
    password: pydantic.SecretStr
    permissions: list[str]

    def is_auth(self, password: pydantic.SecretStr) -> bool:
        return libtools.check_password(password, self.password)


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

    @abc.abstractmethod
    def by_user_id(self, user_id: str) -> ProfileData | None:
        raise NotImplementedError()


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

    @abc.abstractmethod
    def by_username(self, username: str) -> UserData | None:
        raise NotImplementedError()
