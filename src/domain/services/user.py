import enum
from typing import Dict, List

import pydantic


class Role(enum.StrEnum):
    CLIENT = "role:client"
    ADMIN = "role:admin"


class Audience(enum.StrEnum):
    GET_PROFILE = "profile:get"
    UPDATE_PROFILE = "profile:update"

    @staticmethod
    def exists(name: str) -> bool:
        try:
            Audience(name)
        except ValueError:
            return False
        return True


ROLE_PERMISSIONS: Dict[Role, List[Audience]] = {
    Role.ADMIN: [
        # Current Profile
        Audience.GET_PROFILE,
        Audience.UPDATE_PROFILE,
    ],
    Role.CLIENT: [
        # Current Profile
        Audience.GET_PROFILE,
        Audience.UPDATE_PROFILE,
    ],
}


class AuthUser(pydantic.BaseModel):
    id: str
    first_name: str
    last_name: str
    username: str
