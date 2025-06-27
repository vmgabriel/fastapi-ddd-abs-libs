from typing import Dict, List, Type

from src import settings
from src.domain.entrypoint import model
from src.domain.models import repository
from src.domain.models.repository import RepositoryGetter
from src.infra.log import model as log_model
from src.infra.migrator import model as migrator_model


class DomainFactory:
    title: str
    repositories: Dict[str, List[Type[repository.Repository]]]
    entrypoints: Dict[str, List[model.EntrypointModel]]
    migrations: Dict[str, List[migrator_model.MigrateHandler]]
    scripts: Dict[str, List[model.EntrypointModel]]

    def __init__(self, title: str) -> None:
        self.title = title
        self.repositories = {}
        self.entrypoints = {}
        self.migrations = {}
        self.scripts = {}

    def add_repository(
        self,
        repository_provider: str,
        definition_repository: Type[repository.Repository],
    ) -> None:
        if repository_provider not in self.repositories:
            self.repositories[repository_provider] = [definition_repository]
            return
        self.repositories[repository_provider].append(definition_repository)

    def add_entrypoint(
        self, entrypoint_provider: str, entrypoint: model.EntrypointModel
    ) -> None:
        if entrypoint_provider not in self.entrypoints:
            self.entrypoints[entrypoint_provider] = [entrypoint]
            return
        self.entrypoints[entrypoint_provider].append(entrypoint)

    def add_migration(
        self, migration_provider: str, migration: migrator_model.MigrateHandler
    ) -> None:
        if migration_provider not in self.migrations:
            self.migrations[migration_provider] = [migration]
            return
        self.migrations[migration_provider].append(migration)
        
    def add_script(self, script_provider: str, script: model.EntrypointModel) -> None:
        if script_provider not in self.scripts:
            self.scripts[script_provider] = [script]
            return
        self.scripts[script_provider].append(script)


class DomainBuilder:
    configuration: settings.BaseSettings
    logger: log_model.LogAdapter
    domain_factory: DomainFactory

    repository_provider: str
    entrypoint_provider: str

    def __init__(
        self,
        configuration: settings.BaseSettings,
        logger: log_model.LogAdapter,
        domain_factory: DomainFactory,
    ) -> None:
        self.configuration = configuration
        self.logger = logger
        self.domain_factory = domain_factory

        self.repository_provider = configuration.repository_provider
        self.migration_provider = configuration.migrator_provider

    def get_migrations(self) -> List[migrator_model.MigrateHandler]:
        if self.migration_provider not in self.domain_factory.migrations:
            return []
        return self.domain_factory.migrations[self.migration_provider]

    def get_repositories(self) -> repository.RepositoryGetter:
        if self.repository_provider not in self.domain_factory.repositories:
            return RepositoryGetter()
        return RepositoryGetter(
            repositories=self.domain_factory.repositories[self.repository_provider]
        )

    def get_entrypoints(self, entrypoint_provider: str) -> List[model.EntrypointModel]:
        if entrypoint_provider not in self.domain_factory.entrypoints:
            return []
        return self.domain_factory.entrypoints[entrypoint_provider]
    
    def get_scripts(self, script_provider: str) -> List[model.EntrypointModel]:
        if script_provider not in self.domain_factory.scripts:
            return []
        return self.domain_factory.scripts[script_provider]
