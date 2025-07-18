import enum
from typing import Dict, List

import pydantic


class Role(enum.StrEnum):
    CLIENT = "role:client"
    ADMIN = "role:admin"


class Audience(enum.StrEnum):
    GET_PROFILE = "profile:get"
    UPDATE_PROFILE = "profile:update"
    CREATE_TASK = "task:create"
    GET_TASKS = "task:get"
    UPDATE_TASK = "task:update"
    DELETE_TASK = "task:delete"
    CREATE_BOARD = "board:create"
    GET_BOARDS = "board:get"
    UPDATE_BOARD = "board:update"
    DELETE_BOARD = "board:delete"
    CREATE_PROFILE = "profile:create"

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
        Audience.CREATE_BOARD,
    ],
    Role.CLIENT: [
        # Current Profile
        Audience.GET_PROFILE,
        Audience.UPDATE_PROFILE,
        Audience.CREATE_BOARD,
    ],
}


class AuthUser(pydantic.BaseModel):
    id: str
    name: str
    last_name: str
    username: str
