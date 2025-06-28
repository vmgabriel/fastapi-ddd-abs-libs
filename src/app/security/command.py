import uuid
from typing import List

import pydantic

from src.domain import libtools
from src.domain.models import repository as repository_model
from src.domain.models.filter import FilterBuilder
from src.domain.services import command
from src.infra.log import model as log_model
from src.infra.uow.model import UOW
from . import domain as domain_security


class GetDataCommand(command.Command):
    logger: log_model.LogAdapter

    def __init__(self):
        super().__init__(
            requirements=["logger"],
        )

    async def execute(self) -> command.CommandResponse:
        self.logger = self._deps["logger"]
        self.logger.info("Executing GetDataCommand")
        return command.CommandResponse(
            trace_id=getattr(self.request, "trace_id", uuid.uuid4()),
            payload={"message": "ok"},
        )


class CreateSuperUserCommandData(command.CommandRequest):
    name: str
    last_name: str
    username: str
    email: str
    phone: str
    password: pydantic.SecretStr
    repeat_password: pydantic.SecretStr

    @pydantic.model_validator(mode="after")
    def check_passwords_match(self) -> "CreateSuperUserCommandData":
        if self.password != self.repeat_password:
            raise ValueError("Current Password and Repeat Password must match!")
        return self

    def to_repository_user(self, permissions: List[str]) -> domain_security.UserData:
        return domain_security.UserData(
            id=str(uuid.uuid4()),
            name=self.name,
            last_name=self.last_name,
            username=self.username,
            email=self.email,
            password=libtools.encrypt_password(self.password.get_secret_value()),
            permissions=permissions,
        )

    def to_repository_profile(self, user_id: str) -> domain_security.ProfileData:
        return domain_security.ProfileData(
            id=str(uuid.uuid4()),
            user_id=user_id,
            phone=self.phone,
        )


class CreateSuperUserCommand(command.Command):
    logger: log_model.LogAdapter
    repository_getter: repository_model.RepositoryGetter
    uow: UOW
    filter_builder: FilterBuilder

    def __init__(self):
        super().__init__(
            requirements=["logger", "repository_getter", "uow", "filter_builder"],
            request_type=CreateSuperUserCommandData,
        )

    async def execute(self) -> command.CommandResponse:
        self.logger = self._deps["logger"]
        self.repository_getter = self._deps["repository_getter"]
        self.uow = self._deps["uow"]
        self.filter_builder = self._deps["filter_builder"]
        self.logger.info("Executing GetDataCommand")
        self.logger.info(f"Creating Super User {type(self.request)}")

        with self.uow.session() as session:
            repository_user = self.repository_getter(
                repository=domain_security.UserRepository,
                session=session,
            )

            repository_profile = self.repository_getter(
                repository=domain_security.ProfileRepository,
                session=session,
            )

            new_repository_user = repository_user.create(
                new=self.request.to_repository_user(["role:admin"])
            )

            new_repository_data = repository_profile.create(
                new=self.request.to_repository_profile(str(new_repository_user.id))
            )

            session.commit()

        return command.CommandResponse(
            trace_id=getattr(self.request, "trace_id", uuid.uuid4()),
            payload={"message": "ok"},
        )
