from pydantic import BaseModel


class BookScheme(BaseModel):
    title: str
    year_of_pub: int
    url: str = ""
    url_img: str = ""
    num_of_pages: int
    description: str
    publisher: str


class AuthorScheme(BaseModel):
    name: str
    surname: str
