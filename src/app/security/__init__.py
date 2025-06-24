from src.domain.models import domain

from .infra.migrations import migrations as infra_migrations
from .infra.repositories import repositories as infra_repositories


domain_security = domain.DomainFactory()

for migration_provider, migrations in infra_migrations.items():
    for migration in migrations:
        domain_security.add_migration(
            migration_provider=migration_provider, 
            migration=migration
        )
        
for repositories_provider, repositories in infra_repositories.items():
    for repository in repositories:
        domain_security.add_repository(
            repository_provider=repositories_provider, 
            repository=repository
        )