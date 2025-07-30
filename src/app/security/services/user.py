from src.app.security import domain as domain_security
from src.domain.models import repository


def create_user(
    new_user: domain_security.UserData,
    new_profile: domain_security.ProfileData,
    user_repository: domain_security.UserRepository,
    profile_repository: domain_security.ProfileRepository,
) -> repository.RepositoryData:
    if user_repository.by_username(username=new_user.username):
        raise ValueError("Username already exists")
    if user_repository.by_email(email=new_user.email):
        raise ValueError("Email already exists")

    user_data = user_repository.create(new=new_user)
    profile_repository.create(new=new_profile)

    return user_data
