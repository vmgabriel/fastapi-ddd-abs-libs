import datetime
import enum
import uuid
from typing import Dict

import pydantic

from src.domain.models import entity as domain_entity


class TaskStatus(enum.StrEnum):
    TODO = enum.auto()
    DOING = enum.auto()
    DONE = enum.auto()


class TaskHistory(pydantic.BaseModel):
    id: str
    task_id: str
    changed_at: datetime.datetime
    type_of_change: domain_entity.HistoryChangeType
    previous_values: Dict[str, str | None] | None = None
    new_values: Dict[str, str | None] | None = None


class Task(pydantic.BaseModel):
    id: str
    name: str
    description: str
    owner: str
    histories: list[TaskHistory] = pydantic.Field(default_factory=list)
    status: TaskStatus = TaskStatus.TODO
    icon_url: str | None = None

    def require_change(self, status: TaskStatus) -> bool:
        return status is not self.status

    @staticmethod
    def create(
        id: str, name: str, description: str, owner: str, icon_url: str | None = None
    ) -> "Task":
        return Task(
            id=id,
            name=name,
            description=description,
            icon_url=icon_url,
            owner=owner,
            histories=[
                TaskHistory(
                    id=str(uuid.uuid4()),
                    task_id=id,
                    type_of_change=domain_entity.HistoryChangeType.INSERTED,
                    new_values={
                        "id": id,
                        "name": name,
                        "description": description,
                        "icon_url": icon_url,
                        "owner": owner,
                    },
                    changed_at=datetime.datetime.now(),
                )
            ],
        )

    def change_status(self, status: TaskStatus) -> None:
        if status is self.status:
            return

        self.histories.append(
            TaskHistory(
                id=str(uuid.uuid4()),
                task_id=self.id,
                type_of_change=domain_entity.HistoryChangeType.UPDATED,
                changed_at=datetime.datetime.now(),
                previous_values={
                    "status": str(self.status.value),
                },
                new_values={
                    "status": str(status.value),
                },
            )
        )
        self.status = status

    def update(
        self,
        name: str | None = None,
        description: str | None = None,
        icon_url: str | None = None,
    ) -> None:
        if name is None and description is None and icon_url is None:
            return
        current_values: Dict[str, str | None] = {}
        if name is not None:
            current_values["name"] = name
        if description is not None:
            current_values["description"] = description
        if icon_url is not None:
            current_values["icon_url"] = icon_url

        self.histories.append(
            TaskHistory(
                id=str(uuid.uuid4()),
                task_id=self.id,
                type_of_change=domain_entity.HistoryChangeType.UPDATED,
                changed_at=datetime.datetime.now(),
                previous_values={
                    current_value: str(getattr(self, current_value))
                    for current_value in current_values.keys()
                },
                new_values=current_values,
            )
        )
        for key, value in current_values.items():
            setattr(self, key, value)

    def change_owner(self, owner: str) -> None:
        if owner is self.owner:
            return

        self.histories.append(
            TaskHistory(
                id=str(uuid.uuid4()),
                task_id=self.id,
                type_of_change=domain_entity.HistoryChangeType.UPDATED,
                changed_at=datetime.datetime.now(),
                previous_values={
                    "owner": self.owner,
                },
                new_values={
                    "owner": owner,
                },
            )
        )
        self.owner = owner


class Board(pydantic.BaseModel):
    id: str
    name: str
    description: str
    icon_url: str | None = None
    tasks: list[Task] = pydantic.Field(default_factory=list)
    owners: list[str] = pydantic.Field(default_factory=list)

    @staticmethod
    def create(
        id: str, name: str, description: str, user_id: str, icon_url: str | None = None
    ) -> "Board":
        return Board(
            id=id,
            name=name,
            description=description,
            icon_url=icon_url,
            tasks=[],
            owners=[user_id],
        )

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def add_owner(self, user_id: str) -> None:
        self.owners.append(user_id)

    def remove_owner(self, user_id: str) -> None:
        self.owners.remove(user_id)
