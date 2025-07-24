import datetime

import pytest

from src.app.task.domain import entity as subject
from src.domain.models import entity as domain_entity


class TestConstants:
    BOARD_ID = "board-123"
    USER_ID = "user-123"
    ICON_URL = "http://example.com/icon.png"


@pytest.fixture
def task_data():
    return {
        "id": "task-123",
        "name": "Sample Task",
        "description": "A sample task for testing",
        "board_id": TestConstants.BOARD_ID,
        "owner": TestConstants.USER_ID,
        "priority": subject.PriorityType.LOW,
    }


@pytest.fixture
def basic_task(task_data):
    return subject.Task(**task_data)


@pytest.fixture
def board_data():
    return {
        "id": "board-123",
        "name": "Project A",
        "description": "Description of Project A",
        "user_id": TestConstants.USER_ID,
    }


class TestTaskCreation:
    def test_creates_task_with_all_fields(self, task_data):
        task = subject.Task.create(**task_data, icon_url=TestConstants.ICON_URL)
        assert task.id == task_data["id"]
        assert task.name == task_data["name"]
        assert task.description == task_data["description"]
        assert task.icon_url == TestConstants.ICON_URL
        assert task.status == subject.TaskStatus.TODO
        assert task.priority == subject.PriorityType.LOW
        self.verify_creation_history(task, task_data, TestConstants.ICON_URL)

    def test_creates_task_without_icon_url(self, task_data):
        task = subject.Task.create(**task_data)
        assert task.icon_url is None
        self.verify_creation_history(task, task_data, None)

    def verify_creation_history(self, task, data, icon_url):
        assert len(task.histories) == 1
        history = task.histories[0]
        assert history.task_id == data["id"]
        assert history.type_of_change == domain_entity.HistoryChangeType.INSERTED
        assert isinstance(history.id, str) and history.id
        assert isinstance(history.changed_at, datetime.datetime)
        assert history.new_values == {
            "board_id": data["board_id"],
            "priority": data["priority"],
            "id": data["id"],
            "name": data["name"],
            "description": data["description"],
            "icon_url": icon_url,
            "user_id": data["owner"],
        }


class TestTaskStatusChanges:
    def test_changes_status_to_doing(self, basic_task):
        self.verify_status_change(basic_task, subject.TaskStatus.DOING)

    def test_changes_status_to_done(self, basic_task):
        self.verify_status_change(basic_task, subject.TaskStatus.DONE)

    def test_ignores_same_status_change(self, basic_task):
        initial_status = basic_task.status
        basic_task.change_status(initial_status)
        assert basic_task.status == initial_status
        assert len(basic_task.histories) == 0

    def verify_status_change(self, task, new_status):
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
            owner=TestConstants.USER_ID,
            board_id=TestConstants.BOARD_ID,
        )

    def test_updates_single_field(self, updatable_task):
        updates = {"name": "Updated Task"}
        self.verify_task_update(updatable_task, updates)

    def test_updates_multiple_fields(self, updatable_task):
        updates = {
            "name": "Updated Task",
            "description": "Updated Description",
            "icon_url": TestConstants.ICON_URL,
        }
        self.verify_task_update(updatable_task, updates)

    def test_ignores_empty_update(self, updatable_task):
        updatable_task.update()
        assert len(updatable_task.histories) == 0

    def verify_task_update(self, task, updates):
        original_values = {
            "name": task.name,
            "description": task.description,
            "icon_url": task.icon_url,
        }
        task.update(**updates)
        for field, value in updates.items():
            assert getattr(task, field) == value
        self.verify_update_history(task, original_values, updates)

    def verify_update_history(self, task, original_values, updates):
        assert len(task.histories) == 1
        history = task.histories[0]
        assert history.type_of_change == domain_entity.HistoryChangeType.UPDATED
        for field in updates:
            expected = original_values[field]
            actual = history.previous_values[field]
            assert actual == expected or (actual is None and expected is None)
        for field, expected in updates.items():
            actual = history.new_values[field]
            assert actual == expected or (actual is None and expected is None)


class TestBoard:
    def test_create_board_with_all_fields(self, board_data):
        board = subject.Board.create(**board_data, icon_url=TestConstants.ICON_URL)
        self.verify_board_creation(board, board_data, TestConstants.ICON_URL)

    def test_create_board_with_minimum_fields(self, board_data):
        board = subject.Board.create(**board_data)
        self.verify_board_creation(board, board_data, None)

    def verify_board_creation(self, board, data, icon_url):
        assert board.id == data["id"]
        assert board.name == data["name"]
        assert board.description == data["description"]
        assert board.icon_url == icon_url
        assert len(board.members) == 1
        assert board.members[0].user_id == data["user_id"]
        assert board.members[0].board_id == data["id"]
        assert board.tasks == []

    def test_update_board_success(self):
        board_member = subject.BoardMember(
            user_id="user1", board_id="board1", role=subject.RoleMemberType.ADMIN
        )
        board = subject.Board(
            id="board1", name="Old Name", description="Old Description"
        )
        board.inject_member(board_member)

        board.update(
            member_that_update=board_member,
            name="New Name",
            description="New Description",
            icon_url="http://new-icon-url.com",
        )

        assert board.name == "New Name"
        assert board.description == "New Description"
        assert board.icon_url == "http://new-icon-url.com"


class TestAddMember:
    @pytest.fixture
    def board(self):
        return subject.Board(
            id="board-1",
            name="Test Board",
            description="Sample Description",
            icon_url="http://example.com/icon.png",
        )

    @pytest.fixture
    def admin_member(self):
        return subject.BoardMember(
            user_id="admin-user", board_id="board-1", role=subject.RoleMemberType.ADMIN
        )

    @pytest.fixture
    def regular_member(self):
        return subject.BoardMember(
            user_id="regular-user",
            board_id="board-1",
            role=subject.RoleMemberType.VIEWER,
        )

    def test_add_member_success(self, board, admin_member, regular_member):
        board.members.append(admin_member)
        board.add_member(regular_member, member_that_update="admin-user")
        assert regular_member in board.members

    def test_add_member_not_admin(self, board, regular_member):
        with pytest.raises(subject.NotAdminOfBoardError):
            board.add_member(regular_member, member_that_update="non-admin-user")

    def test_add_member_already_exists(self, board, admin_member, regular_member):
        board.members.append(admin_member)
        board.members.append(regular_member)
        with pytest.raises(subject.HasAlreadyIsMemberError):
            board.add_member(regular_member, member_that_update="admin-user")
