from httpx import delete
from sqlalchemy.ext.asyncio import AsyncSession
from books.models import *
from books.schemas import BookScheme, AuthorScheme
from sqlalchemy import select, or_, func, and_


async def search_book_by_title(db: AsyncSession, title: str) -> BookModel:
    result = await db.execute(select(BookModel).filter(BookModel.title == title))

    return result.scalars().first()


async def search_book(db: AsyncSession, book_scheme: BookScheme) -> BookModel:
    result = await db.execute(
        select(BookModel).filter(BookModel.title == book_scheme.title)
    )

    return result.scalars().first()


async def search_author(db: AsyncSession, name: str, surname: str) -> AuthorModel:
    result = await db.execute(
        select(AuthorModel).filter(
            and_(AuthorModel.name == name, AuthorModel.surname == surname)
        )
    )

    return result.scalars().first()


async def search_theme(db: AsyncSession, name: str) -> ThemeModel:
    result = await db.execute(select(ThemeModel).filter(ThemeModel.name == name))

    return result.scalars().first()


async def search_genre(db: AsyncSession, name: str) -> GenreModel:
    result = await db.execute(select(GenreModel).filter(GenreModel.name == name))

    return result.scalars().first()


async def add_book_authors(db: AsyncSession, book_sch: BookScheme, authors: list[str]):
    book = await search_book(db, book_sch)
    book = await db.merge(book)

    for author in authors:
        author_lst = author.split(" ")
        if len(author_lst) > 2:
            author_lst = [" ".join(author_lst[:-1]), author_lst[-1]]
        author_book = await search_author(db, author_lst[0], author_lst[1])
        if not author_book:
            continue
        book_author = BookAuthorModel(id_book=book.id, id_author=author_book.id)
        db.add(book_author)

    await db.commit()


async def add_book_themes(db: AsyncSession, book_sch: BookScheme, themes: list[str]):
    book = await search_book(db, book_sch)
    book = await db.merge(book)

    for theme in themes:
        theme_book = await search_theme(db, theme)
        if not theme_book:
            continue
        book_theme = BookThemeModel(id_book=book.id, id_theme=theme_book.id)
        db.add(book_theme)

    await db.commit()


async def add_book_genres(db: AsyncSession, book_sch: BookScheme, genres: list[str]):
    book = await search_book(db, book_sch)
    book = await db.merge(book)

    for genre in genres:
        genre_book = await search_genre(db, genre)
        if not genre_book:
            continue
        book_genre = BookGenreModel(id_book=book.id, id_genre=genre_book.id)
        db.add(book_genre)

    await db.commit()


async def add_book(
    db: AsyncSession,
    book_scheme: BookScheme,
    authors: list[str],
    themes: list[str],
    genres: list[str],
):
    book = await search_book(db, book_scheme)

    if book:
        return False

    book_model = BookModel(
        title=book_scheme.title,
        year_of_pub=book_scheme.year_of_pub,
        url=book_scheme.url,
        url_img=book_scheme.url_img,
        num_of_pages=book_scheme.num_of_pages,
        description=book_scheme.description,
        publisher=book_scheme.publisher,
    )

    async with db as session:
        session.add(book_model)
        await session.commit()
        await session.refresh(book_model)

    await add_book_authors(db, book_scheme, authors)
    await add_book_themes(db, book_scheme, themes)
    await add_book_genres(db, book_scheme, genres)

    return True


async def get_books_paginated(db: AsyncSession, page: int = 1, page_size: int = 20):

    offset = (page - 1) * page_size

    query = await db.execute(select(BookModel).offset(offset).limit(page_size))

    books = query.scalars().all()

    return books


async def get_authors_substr(db: AsyncSession, substr: str) -> list[AuthorModel]:

    authors = await db.execute(
        select(AuthorModel).where(
            or_(
                func.lower(AuthorModel.name).like(f"%{substr}%"),
                func.lower(AuthorModel.surname).like(f"%{substr}%"),
            )
        )
    )

    return authors.scalars().all()


async def get_authors_of_book(db: AsyncSession, title: str) -> list[AuthorModel]:

    book: BookModel = await search_book_by_title(db, title)

    async with db as session:
        res = await session.execute(
            select(AuthorModel)
            .join(BookAuthorModel, AuthorModel.id == BookAuthorModel.id_author)
            .filter(BookAuthorModel.id_book == book.id)
        )

        authors = res.scalars().all()

        return authors


async def get_genres_of_book(db: AsyncSession, title: str) -> list[str]:

    book: BookModel = await search_book_by_title(db, title)

    async with db as session:
        res = await session.execute(
            select(GenreModel.name)
            .join(BookGenreModel, GenreModel.id == BookGenreModel.id_genre)
            .filter(BookGenreModel.id_book == book.id)
        )

        genres = res.scalars().all()

        return genres


async def get_themes_of_book(db: AsyncSession, title: str) -> list[str]:

    book: BookModel = await search_book_by_title(db, title)

    async with db as session:
        res = await session.execute(
            select(ThemeModel.name)
            .join(BookThemeModel, ThemeModel.id == BookThemeModel.id_theme)
            .filter(BookThemeModel.id_book == book.id)
        )

        themes = res.scalars().all()

        return themes


async def add_author(db: AsyncSession, name: str, surname: str) -> bool:

    async with db as session:
        author = await session.execute(
            select(AuthorModel).where(
                and_(AuthorModel.name == name, AuthorModel.surname == surname)
            )
        )

        if author.scalars().first():
            return False

        author = AuthorModel(name=name, surname=surname)
        session.add(author)
        await session.commit()
        await session.refresh(author)

        return True


async def delete_book(db: AsyncSession, title: str) -> bool:

    book = await search_book_by_title(db, title)

    if not book:
        return False

    await db.delete(book)
    await db.commit()

    return True
