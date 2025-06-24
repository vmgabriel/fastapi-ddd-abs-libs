from typing import Any, List, Dict

from src.infra.migrator import model as mgrator_model
from src.infra.log import model as log_model
from src.domain.models import repository
from src.domain.entrypoint import model

from src import settings


class DomainFactory:
    repositories: Dict[str, List[repository.Repository]]
    entrypoints: Dict[str, List[model.EntrypointModel]]
    migrations: Dict[str, List[mgrator_model.MigrateHandler]]

    def __init__(self) -> None:
        self.repositories = {}
        self.entrypoints = {}
        self.migrations = {}

    def add_repository(
        self, 
        repository_provider: str, 
        repository: repository.Repository
    ) -> None:
        if repository_provider not in self.repositories:
            self.repositories[repository_provider] = [repository]
            return
        self.repositories[repository_provider].append(repository)

    def add_entrypoint(
        self, 
        entrypoint_provider: str, 
        entrypoint: model.EntrypointModel
    ) -> None:
        if entrypoint_provider not in self.entrypoints:
            self.entrypoints[entrypoint_provider] = [entrypoint]
            return
        self.entrypoints[entrypoint_provider].append(entrypoint)
        
    def add_migration(
        self, 
        migration_provider: str, 
        migration: mgrator_model.MigrateHandler
    ) -> None:
        if migration_provider not in self.migrations:
            self.migrations[migration_provider] = [migration]
            return
        self.migrations[migration_provider].append(migration)


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
        
    def get_migrations(self) -> List[mgrator_model.MigrateHandler]:
        if self.migration_provider not in self.domain_factory.migrations:
            return []
        return self.domain_factory.migrations[self.migration_provider]
    
    def get_repositories(self) -> List[repository.Repository]:
        if self.repository_provider not in self.domain_factory.repositories:
            return []
        return self.domain_factory.repositories[self.repository_provider]
    
    def get_entrypoints(self, entrypoint_provider: str) -> List[model.EntrypointModel]:
        if entrypoint_provider not in self.domain_factory.entrypoints:
            return []
        return self.domain_factory.entrypoints[entrypoint_provider]
