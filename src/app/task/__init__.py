from src.domain.models import domain as domain_models

from . import entrypoint
from .infra.migrations import migrations as infra_migrations
from .infra.repositories import repositories as infra_repositories

domain_task = domain_models.DomainFactory("task")

for migration_provider, migrations in infra_migrations.items():
    for migration in migrations:
        domain_task.add_migration(
            migration_provider=migration_provider, migration=migration
        )

for repositories_provider, repositories in infra_repositories.items():
    for repository in repositories:
        domain_task.add_repository(
            repository_provider=repositories_provider, definition_repository=repository
        )

for entrypoint_provider, entrypoints in entrypoint.entrypoints.items():
    for current_entrypoint in entrypoints:
        domain_task.add_entrypoint(
            entrypoint_provider=entrypoint_provider, entrypoint=current_entrypoint
        )
