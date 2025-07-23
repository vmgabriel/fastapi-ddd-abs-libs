from unittest.mock import MagicMock, PropertyMock

from src.app.task.services.task import paginate_task_of_board
from src.domain.models.filter import FilterBuilder, Paginator
from src.domain.services.command import CommandQueryRequest


def test_paginate_task_of_board_valid():
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

    result = paginate_task_of_board(
        board_id, mock_query, mock_repository_task, mock_filter_builder
    )

    assert result == paginator
    assert mock_repository_task.filter.called
    assert mock_filter_builder.build.call_count == 2
    assert mock_filter.update_table.called


def test_paginate_task_of_board_empty_result():
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

    result = paginate_task_of_board(
        board_id, mock_query, mock_repository_task, mock_filter_builder
    )

    assert result == paginator
    assert mock_repository_task.filter.called
    assert mock_filter_builder.build.call_count == 2
    assert mock_filter.update_table.called
