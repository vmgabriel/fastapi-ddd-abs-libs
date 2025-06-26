from typing import List, Type, TypeVar

from src.domain.models.repository import Repository

from .profile import PostgresProfileRepository

ConcreteRepository = TypeVar("ConcreteRepository", bound=Repository)
repositories: List[Type[ConcreteRepository]] = [PostgresProfileRepository]  # type: ignore
