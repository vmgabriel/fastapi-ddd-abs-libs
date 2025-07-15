from typing import Dict


class CustomException(Exception):
    message: str

    def __init__(self, message: str):
        self.message = message

    def to_dict(self) -> Dict[str, str]:
        return {"message": self.message, "type": self.__class__.__name__}
