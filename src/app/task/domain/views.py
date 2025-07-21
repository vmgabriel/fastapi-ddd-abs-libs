import pydantic

from src.app.task.domain.entity import TaskStatus
from src.domain.models import repository as domain_repository


class UserContactMember(pydantic.BaseModel):
    email: str | None = None
    phone: str | None = None


class BoardMember(pydantic.BaseModel):
    contact: UserContactMember
    user_id: str
    icon_url: str | None = None
    full_name: str
    username: str
    role: str


class BoardTaskSummary(pydantic.BaseModel):
    total: int
    active: int
    inactive: int
    summary_status: dict[TaskStatus, int] = pydantic.Field(default_factory=dict)


class DetailedBoard(domain_repository.RepositoryData):
    name: str
    description: str
    icon_url: str | None = None
    members: list[BoardMember] = pydantic.Field(default_factory=list)
    task_summary: BoardTaskSummary
