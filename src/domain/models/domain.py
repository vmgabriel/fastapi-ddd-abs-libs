from typing import Any, List


class DomainFactory:
    repositories: List[Any]
    entrypoints: List[Any]
    migrations: List[Any]

    def __init__(self) -> None:
        self.repositories = []
        self.entrypoints = []
        self.migrations = []

    def add_repository(self, repository) -> None:
        self.repositories.append(repository)

    def add_entrypoint(self, entrypoint) -> None:
        self.entrypoints.append(entrypoint)

    def add_migration(self, migration) -> None:
        self.migrations.append(migration)
