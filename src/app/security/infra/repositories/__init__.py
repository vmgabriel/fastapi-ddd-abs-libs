from typing import Dict, List, Type

from src.domain.models.repository import Repository

from .psycopg import repositories as postgres_repositories

repositories: Dict[str, List[Type[Repository]]] = {
    "psycopg": postgres_repositories,
}
