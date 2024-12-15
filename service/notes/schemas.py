from pydantic import BaseModel


class NoteSchema(BaseModel):
    page: int
    description: str
