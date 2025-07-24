import datetime
import enum
import uuid
from typing import Any, Dict

import pydantic

from src.domain.models import entity as domain_entity
from src.domain.models import exceptions as domain_exceptions
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


class PriorityType(enum.StrEnum):
    LOW = enum.auto()
    MEDIUM = enum.auto()
    HIGH = enum.auto()
    CRITICAL = enum.auto()


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
    priority: PriorityType = PriorityType.LOW
    histories: list[TaskHistory] = pydantic.Field(default_factory=list)
    status: TaskStatus = TaskStatus.TODO
    icon_url: str | None = None
    owner_data: Dict[str, Any] | None = None

    def require_change(self, status: TaskStatus) -> bool:
        return status is not self.status

    @property
    def user_id(self) -> str:
        return self.owner

    @staticmethod
    def create(
        id: str,
        name: str,
        board_id: str,
        description: str,
        owner: str,
        priority: PriorityType = PriorityType.LOW,
        icon_url: str | None = None,
    ) -> "Task":
        return Task(
            id=id,
            name=name,
            board_id=board_id,
            description=description,
            icon_url=icon_url,
            owner=owner,
            priority=priority,
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
                        "user_id": owner,
                        "priority": priority,
                        "board_id": board_id,
                    },
                    changed_at=datetime.datetime.now(),
                )
            ],
        )

    def inject_history(self, history: TaskHistory) -> None:
        self.histories.append(history)

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
        priority: PriorityType | None = None,
    ) -> None:
        if (
            name is None
            and description is None
            and icon_url is None
            and priority is None
        ):
            return
        current_values: Dict[str, str | None] = {}
        if name is not None:
            current_values["name"] = name
        if description is not None:
            current_values["description"] = description
        if icon_url is not None:
            current_values["icon_url"] = icon_url
        if priority is not None:
            current_values["priority"] = priority

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

    def update_role(self, role: RoleMemberType) -> None:
        self.role = role


class IsNotMemberofBoardError(domain_exceptions.CustomException): ...  # noqa: E701


class NotAdminOfBoardError(domain_exceptions.CustomException): ...  # noqa: E701


class IsNotEditorOfBoardError(domain_exceptions.CustomException): ...  # noqa: E701


class HasAlreadyIsMemberError(domain_exceptions.CustomException): ...  # noqa: E701


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

    def get_member_by_user_id(self, user_id: str) -> BoardMember:
        for member in self.members:
            if member.user_id == user_id:
                return member
        raise IsNotMemberofBoardError(f"Member {user_id} not found")

    def is_editor(self, user_id: str) -> bool:
        member = self.get_member_by_user_id(user_id=user_id)
        allowed_roles = [RoleMemberType.EDITOR, RoleMemberType.ADMIN]
        return member.role in allowed_roles

    def is_admin(self, user_id: str) -> bool:
        if not self.is_member(BoardMember(user_id=user_id, board_id=self.id)):
            return False
        return self.get_member_by_user_id(user_id).role == RoleMemberType.ADMIN

    def can_delete(self, user_id: str) -> bool:
        member = self.get_member_by_user_id(user_id=user_id)
        return member.role == RoleMemberType.ADMIN

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

    def add_task(self, task: Task, member_that_insert: str) -> None:
        if not self.is_editor(member_that_insert):
            raise IsNotEditorOfBoardError("Only Editor can add task")
        self.tasks.append(task)

    def inject_member(self, member: BoardMember) -> None:
        self.members.append(member)

    def add_member(
        self,
        member: BoardMember,
        member_that_update: str,
    ) -> None:
        if not self.is_admin(member_that_update):
            raise NotAdminOfBoardError("Only Admin can add members")

        if self.is_member(member):
            raise HasAlreadyIsMemberError(
                f"Member {member.user_id} already in board {self.id}"
            )
        self.members.append(member)

    def remove_member(self, member: BoardMember, member_that_update: str) -> None:
        if not self.is_admin(member_that_update):
            raise NotAdminOfBoardError("Only Admin can add members")

        if not self.is_member(member):
            raise ValueError("I cannot remove member that not in board.")

        if member.user_id == member_that_update:
            raise ValueError("I cannot remove myself")

        self.members.remove(member)

    def update_role_member(
        self, member_that_update: str, member_id: str, role: RoleMemberType
    ) -> None:
        if not self.is_admin(member_that_update):
            raise NotAdminOfBoardError("Only Admin can update role member.")

        member = self.get_member_by_user_id(user_id=member_id)
        if member.role == role:
            return
        member.update_role(role=role)

    def update(
        self,
        member_that_update: BoardMember,
        name: str | None = None,
        description: str | None = None,
        icon_url: str | None = None,
    ) -> None:
        if name is None and description is None and icon_url is None:
            return

        if not self.is_member(member_that_update):
            raise IsNotMemberofBoardError(
                f"Member {member_that_update.user_id} not in board {self.id}"
            )

        if (
            self.get_member_by_user_id(member_that_update.user_id).role
            != RoleMemberType.ADMIN
        ):
            raise NotAdminOfBoardError("Only Admin can update board")

        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if icon_url is not None:
            self.icon_url = icon_url

    def delete(self, user_id: str) -> None:
        if not self.can_delete(user_id=user_id):
            raise NotAdminOfBoardError("Only Admin can delete board")
        self.deleted_at = datetime.datetime.now()
        self.is_activated = False
