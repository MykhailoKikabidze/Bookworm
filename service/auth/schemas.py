from pydantic import BaseModel
from service.abstract_classes import Error


class UsersScheme(BaseModel):
    name: str
    login: str
    password: str
    is_moder: bool


class UserError(Error):
    def __init__(self, message):
        super().__init__(message)

    def get_msg(self):
        super().get_msg()
