from unittest.mock import MagicMock, Mock, PropertyMock

import pytest

from src.app.task.domain import entity as entity_domain
from src.app.task.domain import repository as repository_domain
from src.app.task.domain.entity import Board, Task
from src.app.task.domain.repository import (
    BoardRepository,
    OwnerShipBoardRepository,
    TaskHistoryRepository,
    TaskRepository,
)
from src.app.task.services import task as task_service
from src.app.task.services.task import delete_task
from src.domain.models.filter import FilterBuilder, Paginator
from src.domain.services.command import CommandQueryRequest
from src.infra.log.model import LogAdapter


def paginate_task_of_board_valid():
    board_id = "test_board_id"
    mock_query = MagicMock(spec=CommandQueryRequest)
    type(mock_query).limit = PropertyMock(return_value=10)
    type(mock_query).offset = PropertyMock(return_value=1)
    mock_query.get_filters.return_value = []
    mock_query.get_order_by.return_value = []

    mock_filter = MagicMock()
    mock_filter.update_table = MagicMock()

    mock_repository_task = MagicMock()
    mock_filter_builder = MagicMock(spec=FilterBuilder)
    mock_filter_builder.build.return_value = MagicMock(
        return_value=lambda x: mock_filter
    )

    paginator = Paginator(total=100, page=1, count=10, elements=["task1", "task2"])
    mock_repository_task.filter.return_value = paginator

    result = task_service.paginate_task_of_board(
        board_id, mock_query, mock_repository_task, mock_filter_builder
    )

    assert result == paginator
    assert mock_repository_task.filter.called
    assert mock_filter_builder.build.call_count == 2
    assert mock_filter.update_table.called


def paginate_task_of_board_empty_result():
    board_id = "test_board_id"
    mock_query = MagicMock(spec=CommandQueryRequest)
    type(mock_query).limit = PropertyMock(return_value=10)
    type(mock_query).offset = PropertyMock(return_value=1)
    mock_query.get_filters.return_value = []
    mock_query.get_order_by.return_value = []

    mock_filter = MagicMock()
    mock_filter.update_table = MagicMock()

    mock_repository_task = MagicMock()
    mock_filter_builder = MagicMock(spec=FilterBuilder)
    mock_filter_builder.build.return_value = MagicMock(
        return_value=lambda x: mock_filter
    )

    paginator = Paginator(total=0, page=0, count=0, elements=[])
    mock_repository_task.filter.return_value = paginator

    result = task_service.paginate_task_of_board(
        board_id, mock_query, mock_repository_task, mock_filter_builder
    )

    assert result == paginator
    assert mock_repository_task.filter.called
    assert mock_filter_builder.build.call_count == 2
    assert mock_filter.update_table.called


def create_task_success():
    payload = task_service.CreateTaskCommandRequest(
        id="1",
        name="Test Task",
        description="Task description",
        priority=entity_domain.PriorityType.LOW,
        icon_url="",
    )
    user_id = "123"
    board_id = "456"
    logger = MagicMock(spec=LogAdapter)
    repository_task = MagicMock(spec=repository_domain.TaskRepository)
    repository_task_history = MagicMock(spec=repository_domain.TaskHistoryRepository)
    repository_board = MagicMock(spec=repository_domain.BoardRepository)
    repository_ownership = MagicMock(spec=repository_domain.OwnerShipBoardRepository)

    repository_task.get_by_task_id.return_value = None
    repository_board.get_by_id.return_value = MagicMock()
    repository_ownership.get_by_user_id_and_board_id.return_value = MagicMock()

    result = task_service.create_task(
        payload,
        user_id,
        board_id,
        logger,
        repository_task,
        repository_task_history,
        repository_board,
        repository_ownership,
    )

    assert isinstance(result, entity_domain.Task)
    logger.info.assert_called_once_with("Creating Task")
    repository_task.create.assert_called_once()
    repository_task_history.create.assert_called_once()


def create_task_task_already_exists():
    payload = task_service.CreateTaskCommandRequest(
        id="1",
        name="Test Task",
        description="Task description",
        priority=entity_domain.PriorityType.LOW,
        icon_url="",
    )
    user_id = "123"
    board_id = "456"
    logger = MagicMock(spec=LogAdapter)
    repository_task = MagicMock(spec=repository_domain.TaskRepository)
    repository_task_history = MagicMock(spec=repository_domain.TaskHistoryRepository)
    repository_board = MagicMock(spec=repository_domain.BoardRepository)
    repository_ownership = MagicMock(spec=repository_domain.OwnerShipBoardRepository)

    repository_task.get_by_task_id.return_value = MagicMock()

    with pytest.raises(ValueError, match="Task already exists"):
        task_service.create_task(
            payload,
            user_id,
            board_id,
            logger,
            repository_task,
            repository_task_history,
            repository_board,
            repository_ownership,
        )

    logger.info.assert_not_called()


def create_task_board_not_found():
    payload = task_service.CreateTaskCommandRequest(
        id="1",
        name="Test Task",
        description="Task description",
        priority=entity_domain.PriorityType.LOW,
        icon_url="",
    )
    user_id = "123"
    board_id = "456"
    logger = MagicMock(spec=LogAdapter)
    repository_task = MagicMock(spec=repository_domain.TaskRepository)
    repository_task_history = MagicMock(spec=repository_domain.TaskHistoryRepository)
    repository_board = MagicMock(spec=repository_domain.BoardRepository)
    repository_ownership = MagicMock(spec=repository_domain.OwnerShipBoardRepository)

    repository_task.get_by_task_id.return_value = None
    repository_board.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Board not found"):
        task_service.create_task(
            payload,
            user_id,
            board_id,
            logger,
            repository_task,
            repository_task_history,
            repository_board,
            repository_ownership,
        )


# Update


def test_update_task_success():
    mock_logger = MagicMock(spec=LogAdapter)
    mock_task_repo = MagicMock(spec=repository_domain.TaskRepository)
    mock_task_history_repo = MagicMock(spec=repository_domain.TaskHistoryRepository)
    mock_board_repo = MagicMock(spec=repository_domain.BoardRepository)
    mock_ownership_repo = MagicMock(spec=repository_domain.OwnerShipBoardRepository)

    mock_task = MagicMock(spec=entity_domain.Task)
    mock_task.histories = [MagicMock()]
    mock_task.board_id = "board_1"

    mock_board = MagicMock(spec=entity_domain.Board)

    mock_task_repo.get_by_id.return_value = mock_task
    mock_board_repo.get_by_id.return_value = mock_board

    payload = task_service.UpdateTaskCommandRequest(
        name="Updated Task",
        description="Updated Description",
        priority=entity_domain.PriorityType.HIGH,
        icon_url=None,
    )

    result = task_service.update_task(
        id="task_1",
        user_id="user_1",
        payload=payload,
        logger=mock_logger,
        repository_task=mock_task_repo,
        repository_task_history=mock_task_history_repo,
        repository_board=mock_board_repo,
        repository_ownership=mock_ownership_repo,
    )

    assert result == mock_task
    mock_logger.info.assert_called_once_with("Updating Task")
    mock_task.update.assert_called_once_with(
        name="Updated Task",
        description="Updated Description",
        priority=entity_domain.PriorityType.HIGH,
        icon_url=None,
    )
    mock_board.update_task.assert_called_once_with(
        task=mock_task, member_that_update="user_1"
    )
    mock_task_repo.update.assert_called_once_with(id="task_1", to_update=mock_task)
    mock_task_history_repo.create.assert_called_once_with(new=mock_task.histories[-1])


def test_update_task_raises_task_not_found():
    mock_logger = MagicMock(spec=LogAdapter)
    mock_task_repo = MagicMock(spec=repository_domain.TaskRepository)
    mock_task_history_repo = MagicMock(spec=repository_domain.TaskHistoryRepository)
    mock_board_repo = MagicMock(spec=repository_domain.BoardRepository)
    mock_ownership_repo = MagicMock(spec=repository_domain.OwnerShipBoardRepository)

    mock_task_repo.get_by_id.return_value = None

    payload = task_service.UpdateTaskCommandRequest(
        name="Updated Task",
        description="Updated Description",
        priority=entity_domain.PriorityType.HIGH,
        icon_url=None,
    )

    with pytest.raises(ValueError, match="Task not found"):
        task_service.update_task(
            id="task_1",
            user_id="user_1",
            payload=payload,
            logger=mock_logger,
            repository_task=mock_task_repo,
            repository_task_history=mock_task_history_repo,
            repository_board=mock_board_repo,
            repository_ownership=mock_ownership_repo,
        )


def test_update_task_raises_board_not_found():
    mock_logger = MagicMock(spec=LogAdapter)
    mock_task_repo = MagicMock(spec=repository_domain.TaskRepository)
    mock_task_history_repo = MagicMock(spec=repository_domain.TaskHistoryRepository)
    mock_board_repo = MagicMock(spec=repository_domain.BoardRepository)
    mock_ownership_repo = MagicMock(spec=repository_domain.OwnerShipBoardRepository)

    mock_task = MagicMock(spec=entity_domain.Task)
    mock_task.board_id = "board_1"

    mock_task_repo.get_by_id.return_value = mock_task
    mock_board_repo.get_by_id.return_value = None

    payload = task_service.UpdateTaskCommandRequest(
        name="Updated Task",
        description="Updated Description",
        priority=entity_domain.PriorityType.HIGH,
        icon_url=None,
    )

    with pytest.raises(ValueError, match="Board not found"):
        task_service.update_task(
            id="task_1",
            user_id="user_1",
            payload=payload,
            logger=mock_logger,
            repository_task=mock_task_repo,
            repository_task_history=mock_task_history_repo,
            repository_board=mock_board_repo,
            repository_ownership=mock_ownership_repo,
        )


def test_delete_task_success():
    # Arrange
    mock_logger = Mock(spec=LogAdapter)
    mock_repository_task = Mock(spec=TaskRepository)
    mock_repository_task_history = Mock(spec=TaskHistoryRepository)
    mock_repository_board = Mock(spec=BoardRepository)
    mock_repository_ownership = Mock(spec=OwnerShipBoardRepository)

    task_id = "test_task_id"
    user_id = "test_user_id"

    mock_task = Mock(spec=Task)
    mock_task.board_id = "test_board_id"
    mock_task.histories = []
    type(mock_task).histories = PropertyMock(return_value=[Mock()])

    mock_board = Mock(spec=Board)
    mock_board.owners = []
    mock_board.members = []
    mock_board.is_member = Mock(return_value=True)
    mock_board.delete_task = Mock()

    mock_repository_task.get_by_id.return_value = mock_task
    mock_repository_board.get_by_id.return_value = mock_board
    mock_repository_ownership.get_by_board_id.return_value = []
    mock_repository_task_history.get_by_task_id.return_value = []

    # Act
    result = delete_task(
        id=task_id,
        user_id=user_id,
        logger=mock_logger,
        repository_task=mock_repository_task,
        repository_task_history=mock_repository_task_history,
        repository_board=mock_repository_board,
        repository_ownership=mock_repository_ownership,
    )

    # Assert
    assert result == mock_task
    mock_logger.info.assert_called_with("Deleting Task")
    mock_task.delete.assert_called_once()
    mock_board.delete_task.assert_called_once_with(
        task=mock_task, member_that_delete=user_id
    )
    mock_repository_task.delete.assert_called_once_with(id=task_id)
    mock_repository_task_history.create.assert_called_once()


def test_delete_task_not_found():
    mock_logger = Mock(spec=LogAdapter)
    mock_repository_task = Mock(spec=TaskRepository)
    mock_repository_task_history = Mock(spec=TaskHistoryRepository)
    mock_repository_board = Mock(spec=BoardRepository)
    mock_repository_ownership = Mock(spec=OwnerShipBoardRepository)

    task_id = "non_existent_task_id"
    user_id = "test_user_id"

    mock_repository_task.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Task not found"):
        delete_task(
            id=task_id,
            user_id=user_id,
            logger=mock_logger,
            repository_task=mock_repository_task,
            repository_task_history=mock_repository_task_history,
            repository_board=mock_repository_board,
            repository_ownership=mock_repository_ownership,
        )


def test_delete_task_board_not_found():
    # Arrange
    mock_logger = MagicMock(spec=LogAdapter)
    mock_task_repo = MagicMock(spec=repository_domain.TaskRepository)
    mock_task_history_repo = MagicMock(spec=repository_domain.TaskHistoryRepository)
    mock_board_repo = MagicMock(spec=repository_domain.BoardRepository)
    mock_ownership_repo = MagicMock(spec=repository_domain.OwnerShipBoardRepository)

    mock_task = MagicMock(spec=entity_domain.Task)
    mock_task.board_id = "board_1"
    mock_task.histories = []

    mock_task_repo.get_by_id.return_value = mock_task
    mock_board_repo.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(ValueError, match="Board not found"):
        task_service.delete_task(
            id="task_1",
            user_id="user_1",
            logger=mock_logger,
            repository_task=mock_task_repo,
            repository_task_history=mock_task_history_repo,
            repository_board=mock_board_repo,
            repository_ownership=mock_ownership_repo,
        )

    mock_task_repo.get_by_id.assert_called_once_with(id="task_1")
    mock_board_repo.get_by_id.assert_called_once_with(id="board_1")
