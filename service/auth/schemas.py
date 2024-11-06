from typing import Optional

from pydantic import BaseModel
from abstract_classes import Error


class UsersScheme(BaseModel):
    name: str
    login: str
    password: Optional[str] = None
    is_moder: bool


class UserError(Error):
    def __init__(self, message):
        super().__init__(message)

    def get_msg(self):
        super().get_msg()
