from pydantic import BaseModel


class NoteSchema(BaseModel):
    page: int
    description: str
    quote: str
    character: str


class GroupSchema(BaseModel):
    is_favourite: bool
    want_to_read: bool
    now_reading: bool
    have_read: bool
