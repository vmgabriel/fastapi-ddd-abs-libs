import datetime

import pytest

from src.app.task.domain import entity as subject
from src.domain.models import entity as domain_entity

# Environment Variable
TEST_BOARD_ID = "board-123"
TEST_USER_ID = "user-123"
TEST_ICON_URL = "http://example.com/icon.png"


@pytest.fixture
def task_data():
    return {
        "id": "task-123",
        "name": "Sample Task",
        "description": "A sample task for testing",
        "board_id": TEST_BOARD_ID,
        "owner": TEST_USER_ID,
    }


@pytest.fixture
def basic_task(task_data):
    return subject.Task(**task_data)


class TestTaskCreation:
    def test_creates_task_with_all_fields(self, task_data):
        task = subject.Task.create(**task_data, icon_url=TEST_ICON_URL)

        assert task.id == task_data["id"]
        assert task.name == task_data["name"]
        assert task.description == task_data["description"]
        assert task.icon_url == TEST_ICON_URL

        self._assert_valid_creation_history(task, task_data, TEST_ICON_URL)

    def test_creates_task_without_icon_url(self, task_data):
        task = subject.Task.create(**task_data)

        assert task.icon_url is None
        self._assert_valid_creation_history(task, task_data, None)

    def _assert_valid_creation_history(self, task, data, icon_url):
        assert len(task.histories) == 1
        history = task.histories[0]
        assert history.task_id == data["id"]
        assert history.type_of_change == domain_entity.HistoryChangeType.INSERTED
        assert isinstance(history.id, str) and history.id
        assert isinstance(history.changed_at, datetime.datetime)
        assert history.new_values == {
            "id": data["id"],
            "name": data["name"],
            "description": data["description"],
            "icon_url": icon_url,
            "owner": data["owner"],
        }


class TestTaskStatusChanges:
    def test_changes_status_to_doing(self, basic_task):
        self._assert_status_change(basic_task, subject.TaskStatus.DOING)

    def test_changes_status_to_done(self, basic_task):
        self._assert_status_change(basic_task, subject.TaskStatus.DONE)

    def test_ignores_same_status_change(self, basic_task):
        initial_status = basic_task.status
        basic_task.change_status(initial_status)

        assert basic_task.status == initial_status
        assert len(basic_task.histories) == 0

    def _assert_status_change(self, task, new_status):
        old_status = task.status
        task.change_status(new_status)

        assert task.status == new_status
        assert len(task.histories) == 1
        history = task.histories[0]
        assert history.previous_values["status"] == old_status.value
        assert history.new_values["status"] == new_status.value


class TestTaskUpdates:
    @pytest.fixture
    def updatable_task(self):
        return subject.Task(
            id="update-123",
            name="Original Task",
            description="Original Description",
            icon_url=None,
            owner=TEST_USER_ID,
            board_id=TEST_BOARD_ID,
        )

    def test_updates_single_field(self, updatable_task):
        updates = {"name": "Updated Task"}
        self._assert_task_update(updatable_task, updates)

    def test_updates_multiple_fields(self, updatable_task):
        updates = {
            "name": "Updated Task",
            "description": "Updated Description",
            "icon_url": TEST_ICON_URL,
        }
        self._assert_task_update(updatable_task, updates)

    def test_ignores_empty_update(self, updatable_task):
        updatable_task.update()
        assert len(updatable_task.histories) == 0

    def _assert_task_update(self, task, updates):
        original_values = {
            "name": task.name,
            "description": task.description,
            "icon_url": task.icon_url,
        }

        task.update(**updates)

        for field, value in updates.items():
            assert getattr(task, field) == value

        assert len(task.histories) == 1
        history = task.histories[0]
        assert history.type_of_change == domain_entity.HistoryChangeType.UPDATED

        for field in updates:
            expected = original_values[field]
            actual = history.previous_values[field]
            if expected is None:
                assert actual is None, (
                    f"Expected None for {field}-[type({type(field)})]],"
                    f" but got {actual}-[type({type(actual)})]"
                )
            else:
                assert actual == expected, f"Mismatch in previous values for {field}"

        for field, expected in updates.items():
            actual = history.new_values[field]
            if expected is None:
                assert actual is None, f"Expected None for {field}, but got {actual}"
            else:
                assert actual == expected, f"Mismatch in new values for {field}"


# Board


def test_create_board_with_all_fields():
    board = subject.Board.create(
        id="1",
        name="Project A",
        description="Description of Project A",
        icon_url="http://example.com/icon.png",
        user_id="user_id",
    )
    assert board.id == "1"
    assert len(board.owners) == 1
    assert board.owners[0] == "user_id"
    assert board.name == "Project A"
    assert board.description == "Description of Project A"
    assert board.icon_url == "http://example.com/icon.png"
    assert board.tasks == []


def test_create_board_with_minimum_fields():
    board = subject.Board.create(
        id="2",
        name="Project B",
        description="Description of Project B",
        user_id="user_id",
    )
    assert board.id == "2"
    assert board.name == "Project B"
    assert board.description == "Description of Project B"
    assert board.icon_url is None
    assert board.tasks == []
    assert len(board.owners) == 1
    assert board.owners[0] == "user_id"
