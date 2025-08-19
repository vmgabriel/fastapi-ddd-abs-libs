import enum
from typing import Dict, List

import pydantic


class Role(enum.StrEnum):
    CLIENT = "role:client"
    ADMIN = "role:admin"


class Audience(enum.StrEnum):
    GET_PROFILE = "profile:get"
    UPDATE_PROFILE = "profile:update"
    CREATE_PROFILE = "profile:create"

    CREATE_TASK = "task:create"
    GET_TASK = "task:get"
    GET_TASKS = "task:gets"
    GET_TASKS_ALL = "task:gets_all"
    UPDATE_TASK = "task:update"
    DELETE_TASK = "task:delete"
    CREATE_BOARD = "board:create"
    GET_BOARDS = "board:gets"
    GET_BOARD = "board:get"
    UPDATE_BOARD = "board:update"
    DELETE_BOARD = "board:delete"
    ADD_MEMBER_BOARD = "board:add_member"
    REMOVE_MEMBER_BOARD = "board:remove_member"
    UPDATE_ROLE_MEMBER_BOARD = "board:update_role_member"

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
        # Task
        Audience.CREATE_BOARD,
        Audience.GET_BOARD,
        Audience.GET_BOARDS,
        Audience.UPDATE_BOARD,
        Audience.DELETE_BOARD,
        Audience.ADD_MEMBER_BOARD,
        Audience.REMOVE_MEMBER_BOARD,
        Audience.UPDATE_ROLE_MEMBER_BOARD,
        Audience.GET_TASKS,
        Audience.CREATE_TASK,
        Audience.GET_TASK,
        Audience.UPDATE_TASK,
        Audience.DELETE_TASK,
        Audience.GET_TASKS_ALL,
    ],
    Role.CLIENT: [
        # Current Profile
        Audience.GET_PROFILE,
        Audience.UPDATE_PROFILE,
        # Task
        Audience.CREATE_BOARD,
        Audience.GET_BOARD,
        Audience.GET_BOARDS,
        Audience.UPDATE_BOARD,
        Audience.DELETE_BOARD,
        Audience.ADD_MEMBER_BOARD,
        Audience.REMOVE_MEMBER_BOARD,
        Audience.UPDATE_ROLE_MEMBER_BOARD,
        Audience.GET_TASKS,
        Audience.CREATE_TASK,
        Audience.GET_TASK,
        Audience.UPDATE_TASK,
        Audience.DELETE_TASK,
        Audience.GET_TASKS_ALL,
    ],
}


class AuthUser(pydantic.BaseModel):
    id: str
    name: str
    last_name: str
    username: str
