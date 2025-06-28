from typing import List, Type, TypeVar

from src.domain.models.repository import Repository
from .profile import PostgresProfileRepository
from .user import PostgresUserRepository

ConcreteRepository = TypeVar("ConcreteRepository", bound=Repository)
repositories: List[Type[ConcreteRepository]] = [  # type: ignore
    PostgresProfileRepository,
    PostgresUserRepository,
]  # type: ignore
