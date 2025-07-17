import datetime

import pytest

from src.app.task.domain import entity as subject
from src.domain.models import entity as domain_entity


@pytest.fixture
def task():
    return subject.Task(
        id="123",
        name="Sample Task",
        description="A sample task for testing",
        status=subject.TaskStatus.TODO,
    )


# Task


def test_task_creation():
    task_id = "12345"
    name = "Test Task"
    description = "This is a test task"
    icon_url = "http://example.com/icon.png"

    task = subject.Task.create(
        id=task_id, name=name, description=description, icon_url=icon_url
    )

    assert task.id == task_id
    assert task.name == name
    assert task.description == description
    assert task.icon_url == icon_url
    assert len(task.histories) == 1
    history = task.histories[0]
    assert history.task_id == task_id
    assert history.type_of_change == domain_entity.HistoryChangeType.INSERTED
    assert history.new_values == {
        "id": task_id,
        "name": name,
        "description": description,
        "icon_url": icon_url,
    }
    assert isinstance(history.changed_at, datetime.datetime)


def test_task_creation_without_icon_url():
    task_id = "67890"
    name = "Task Without Icon"
    description = "A task without an icon URL"

    task = subject.Task.create(id=task_id, name=name, description=description)

    assert task.id == task_id
    assert task.name == name
    assert task.description == description
    assert task.icon_url is None
    assert len(task.histories) == 1
    history = task.histories[0]
    assert history.task_id == task_id
    assert history.type_of_change == domain_entity.HistoryChangeType.INSERTED
    assert history.new_values == {
        "id": task_id,
        "name": name,
        "description": description,
        "icon_url": None,
    }
    assert isinstance(history.changed_at, datetime.datetime)


def test_task_history_has_unique_id():
    task_id = "abcdef"
    name = "Unique Task"
    description = "Task to test unique history ID"

    task = subject.Task.create(id=task_id, name=name, description=description)

    history_id = task.histories[0].id
    assert isinstance(history_id, str)
    assert history_id != ""


def test_change_status_to_doing(task):
    new_status = subject.TaskStatus.DOING
    task.change_status(new_status)
    assert task.status == new_status
    assert len(task.histories) == 1
    assert task.histories[0].new_values["status"] == new_status.value


def test_change_status_to_done(task):
    new_status = subject.TaskStatus.DONE
    task.change_status(new_status)
    assert task.status == new_status
    assert len(task.histories) == 1
    assert task.histories[0].previous_values["status"] == subject.TaskStatus.TODO.value


def test_no_status_change(task):
    old_status = task.status
    task.change_status(task.status)
    assert task.status == old_status
    assert len(task.histories) == 0


def test_update_with_name_only():
    task = subject.Task(
        id="1", name="Original Task", description="Original Description"
    )
    new_name = "Updated Task"

    task.update(name=new_name)

    assert task.name == new_name
    assert task.description == "Original Description"
    assert len(task.histories) == 1
    assert task.histories[0].type_of_change == domain_entity.HistoryChangeType.UPDATED
    assert task.histories[0].previous_values["name"] == "Original Task"
    assert task.histories[0].new_values["name"] == new_name


def test_update_with_description_only():
    task = subject.Task(
        id="2", name="Original Task", description="Original Description"
    )
    new_description = "Updated Description"

    task.update(description=new_description)

    assert task.name == "Original Task"
    assert task.description == new_description
    assert len(task.histories) == 1
    assert task.histories[0].type_of_change == domain_entity.HistoryChangeType.UPDATED
    assert task.histories[0].previous_values["description"] == "Original Description"
    assert task.histories[0].new_values["description"] == new_description


def test_update_with_icon_url_only():
    task = subject.Task(
        id="3", name="Original Task", description="Original Description"
    )
    new_icon_url = "http://example.com/icon.png"

    task.update(icon_url=new_icon_url)

    assert task.icon_url == new_icon_url
    assert len(task.histories) == 1
    assert task.histories[0].type_of_change == domain_entity.HistoryChangeType.UPDATED
    assert task.histories[0].new_values["icon_url"] == new_icon_url


def test_update_no_changes():
    task = subject.Task(
        id="4", name="Original Task", description="Original Description"
    )

    task.update()

    assert task.name == "Original Task"
    assert task.description == "Original Description"
    assert len(task.histories) == 0


def test_update_multiple_fields():
    task = subject.Task(
        id="5", name="Original Task", description="Original Description"
    )
    new_name = "Updated Task"
    new_description = "Updated Description"
    new_icon_url = "http://example.com/icon_updated.png"

    task.update(name=new_name, description=new_description, icon_url=new_icon_url)

    assert task.name == new_name
    assert task.description == new_description
    assert task.icon_url == new_icon_url
    assert len(task.histories) == 1
    assert task.histories[0].type_of_change == domain_entity.HistoryChangeType.UPDATED
    assert task.histories[0].previous_values["name"] == "Original Task"
    assert task.histories[0].previous_values["description"] == "Original Description"
    assert task.histories[0].new_values["name"] == new_name
    assert task.histories[0].new_values["description"] == new_description
    assert task.histories[0].new_values["icon_url"] == new_icon_url


# Board


def test_create_board_with_all_fields():
    board = subject.Board.create(
        id="1",
        name="Project A",
        description="Description of Project A",
        icon_url="http://example.com/icon.png",
    )
    assert board.id == "1"
    assert board.name == "Project A"
    assert board.description == "Description of Project A"
    assert board.icon_url == "http://example.com/icon.png"
    assert board.tasks == []


def test_create_board_with_minimum_fields():
    board = subject.Board.create(
        id="2", name="Project B", description="Description of Project B"
    )
    assert board.id == "2"
    assert board.name == "Project B"
    assert board.description == "Description of Project B"
    assert board.icon_url is None
    assert board.tasks == []
