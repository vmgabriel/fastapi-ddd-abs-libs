import abc

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
