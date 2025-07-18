from typing import List, Type, TypeVar

from src.domain.models.repository import Repository

from .board import PostgresBoardRepository, PostgresOwnerShipBoardRepository
from .task import PostgresHistoryTaskRepository, PostgresTaskRepository

ConcreteRepository = TypeVar("ConcreteRepository", bound=Repository)
repositories: List[Type[ConcreteRepository]] = [  # type: ignore
    PostgresTaskRepository,
    PostgresHistoryTaskRepository,
    PostgresBoardRepository,
    PostgresOwnerShipBoardRepository,
]  # type: ignore
