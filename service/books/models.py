from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base


class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, index=True, unique=True)
    year_of_pub = Column(Integer, index=True)
    url = Column(String)
    url_img = Column(String)
    num_of_pages = Column(Integer)
    description = Column(String)
    publisher = Column(String)

    themes = relationship(
        "ThemeModel", secondary="books_themes", back_populates="books"
    )
    authors = relationship(
        "AuthorModel", secondary="books_authors", back_populates="books"
    )
    genres = relationship(
        "GenreModel", secondary="books_genres", back_populates="books"
    )
    users_checkpoints = relationship(
        "UsersModel", secondary="checkpoints", back_populates="books_checkpoints"
    )
    users_notes = relationship(
        "UsersModel", secondary="notes", back_populates="books_notes"
    )


class ThemeModel(Base):
    __tablename__ = "themes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True, unique=True)

    books = relationship("BookModel", secondary="books_themes", back_populates="themes")


class BookThemeModel(Base):
    __tablename__ = "books_themes"

    id_book = Column(
        Integer, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True
    )
    id_theme = Column(
        Integer, ForeignKey("themes.id", ondelete="CASCADE"), primary_key=True
    )


class AuthorModel(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)

    books = relationship(
        "BookModel", secondary="books_authors", back_populates="authors"
    )


class BookAuthorModel(Base):
    __tablename__ = "books_authors"

    id_book = Column(
        Integer, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True
    )
    id_author = Column(
        Integer, ForeignKey("authors.id", ondelete="CASCADE"), primary_key=True
    )


class GenreModel(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True, unique=True)

    books = relationship("BookModel", secondary="books_genres", back_populates="genres")


class BookGenreModel(Base):
    __tablename__ = "books_genres"

    id_book = Column(
        Integer, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True
    )
    id_genre = Column(
        Integer, ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True
    )
