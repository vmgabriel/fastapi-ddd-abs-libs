from typing import cast

from src.app.security import domain as domain_security
from src.domain.models import repository as repository_model


def find_user_by_email(
    email: str,
    user_repository: domain_security.UserRepository,
) -> domain_security.UserData | None:
    return user_repository.by_email(email=email)


def find_user_by_username(
    username: str,
    user_repository: domain_security.UserRepository,
) -> domain_security.UserData | None:
    return user_repository.by_username(username=username)


def find_user_by_id(
    id: str,
    user_repository: domain_security.UserRepository,
) -> domain_security.UserData | None:
    try:
        return cast(domain_security.UserData | None, user_repository.get_by_id(id=id))
    except repository_model.RepositoryNotFoundError:
        return None
