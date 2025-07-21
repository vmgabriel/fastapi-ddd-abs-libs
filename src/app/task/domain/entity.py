import datetime
import enum
import uuid
from typing import Dict

import pydantic

from src.domain.models import entity as domain_entity
from src.domain.models import repository as domain_repository


class TaskStatus(enum.StrEnum):
    TODO = enum.auto()
    DOING = enum.auto()
    DONE = enum.auto()
    ABANDONED = enum.auto()


class RoleMemberType(enum.StrEnum):
    EDITOR = enum.auto()
    VIEWER = enum.auto()
    ADMIN = enum.auto()


class TaskHistory(domain_repository.RepositoryData):
    task_id: str
    changed_at: datetime.datetime
    type_of_change: domain_entity.HistoryChangeType
    previous_values: Dict[str, str | None] | None = None
    new_values: Dict[str, str | None] | None = None


class Task(domain_repository.RepositoryData):
    name: str
    board_id: str
    description: str
    owner: str
    histories: list[TaskHistory] = pydantic.Field(default_factory=list)
    status: TaskStatus = TaskStatus.TODO
    icon_url: str | None = None

    def require_change(self, status: TaskStatus) -> bool:
        return status is not self.status

    @staticmethod
    def create(
        id: str,
        name: str,
        board_id: str,
        description: str,
        owner: str,
        icon_url: str | None = None,
    ) -> "Task":
        return Task(
            id=id,
            name=name,
            board_id=board_id,
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
                    current_value: (
                        str(getattr(self, current_value))
                        if getattr(self, current_value)
                        else None
                    )
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


class BoardMember(pydantic.BaseModel):
    user_id: str
    board_id: str
    role: RoleMemberType = RoleMemberType.VIEWER

    def __eq__(self, other: object) -> bool:
        return self.user_id == getattr(
            other, "user_id", ""
        ) and self.board_id == getattr(other, "board_id", "")


class Board(domain_repository.RepositoryData):
    name: str
    description: str
    icon_url: str | None = None
    tasks: list[Task] = pydantic.Field(default_factory=list)
    members: list[BoardMember] = pydantic.Field(default_factory=list)

    def is_member(self, member: BoardMember) -> bool:
        return any(
            check_member.user_id == member.user_id for check_member in self.members
        )

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
            members=[
                BoardMember(user_id=user_id, board_id=id, role=RoleMemberType.ADMIN)
            ],
        )

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def add_member(self, member: BoardMember) -> None:
        self.members.append(member)

    def remove_member(self, member: BoardMember) -> None:
        self.members.remove(member)
