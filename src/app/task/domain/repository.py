import abc
from typing import List

from src.domain.models import mixin, repository


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


class OwnerShipRepositoryData(repository.RepositoryData):
    user_id: str
    board_id: str


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
