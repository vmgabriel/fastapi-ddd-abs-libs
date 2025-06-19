from typing import Any, List


class DomainFactory:
    repositories: List[Any]
    entrypoints: List[Any]

    def __init__(self) -> None:
        self.repositories = []
        self.entrypoints = []

    def add_repository(self, repository) -> None:
        self.repositories.append(repository)

    def add_entrypoint(self, entrypoint) -> None:
        self.entrypoints.append(entrypoint)
