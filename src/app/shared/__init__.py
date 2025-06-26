from src.domain.models import domain as domain_models

from . import entrypoint

domain_shared = domain_models.DomainFactory("Shared")


for entrypoint_provider, entrypoints in entrypoint.entrypoints.items():
    for current_entrypoint in entrypoints:
        domain_shared.add_entrypoint(
            entrypoint_provider=entrypoint_provider, entrypoint=current_entrypoint
        )
