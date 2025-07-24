import abc
from typing import List

from src.domain.models import filter as filter_domain
from src.domain.models import mixin, repository

from . import entity as entity_domain


class BoardRepository(
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
    def filter_by_user_id(
        self, user_id: str, criteria: filter_domain.Criteria
    ) -> filter_domain.Paginator:
        raise NotImplementedError()


class TaskRepository(
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


class TaskHistoryRepository(
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
    def get_by_task_id(self, task_id: str) -> List[entity_domain.TaskHistory]:
        raise NotImplementedError()


class OwnerShipRepositoryData(repository.RepositoryData):
    user_id: str
    board_id: str
    role: entity_domain.RoleMemberType


class OwnerShipBoardRepository(
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
    def get_by_user_id_and_board_id(
        self, user_id: str, board_id: str
    ) -> OwnerShipRepositoryData | None:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_by_board_id(self, board_id: str) -> List[OwnerShipRepositoryData]:
        raise NotImplementedError()

    @abc.abstractmethod
    def delete_by_user_id_and_board_id(self, user_id: str, board_id: str) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def update_role_by_user_id_and_board_id(
        self, user_id: str, board_id: str, to_update: entity_domain.RoleMemberType
    ) -> None:
        raise NotImplementedError()


class DetailedBoardRepository(
    repository.Repository,
    mixin.GetterMixin,
    mixin.GetterListMixin,
    abc.ABC,
):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @abc.abstractmethod
    def filter_by_user_id(
        self, user_id: str, criteria: filter_domain.Criteria
    ) -> filter_domain.Paginator:
        raise NotImplementedError()
