from unittest.mock import MagicMock, PropertyMock

import pytest

from src.app.task.domain import repository as repository_domain
from src.app.task.domain.entity import PriorityType, Task
from src.app.task.services import task as task_service
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
        priority=PriorityType.LOW,
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

    assert isinstance(result, Task)
    logger.info.assert_called_once_with("Creating Task")
    repository_task.create.assert_called_once()
    repository_task_history.create.assert_called_once()


def create_task_task_already_exists():
    payload = task_service.CreateTaskCommandRequest(
        id="1",
        name="Test Task",
        description="Task description",
        priority=PriorityType.LOW,
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
        priority=PriorityType.LOW,
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
