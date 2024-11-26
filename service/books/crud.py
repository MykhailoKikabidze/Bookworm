from sqlalchemy.ext.asyncio import AsyncSession
from books.models import *
from books.schemas import BookScheme
from sqlalchemy import select


async def search_book_by_title(db: AsyncSession, title: str) -> BookModel:
    result = await db.execute(select(BookModel).filter(BookModel.title == title))

    return result.scalars().first()


async def search_book(db: AsyncSession, book_scheme: BookScheme) -> BookModel:
    result = await db.execute(
        select(BookModel).filter(BookModel.title == book_scheme.title)
    )

    return result.scalars().first()


async def search_author(db: AsyncSession, name: str) -> AuthorModel:
    result = await db.execute(select(AuthorModel).filter(AuthorModel.name == name))

    return result.scalars().first()


async def search_theme(db: AsyncSession, name: str) -> ThemeModel:
    result = await db.execute(select(ThemeModel).filter(ThemeModel.name == name))

    return result.scalars().first()


async def search_genre(db: AsyncSession, name: str) -> GenreModel:
    result = await db.execute(select(GenreModel).filter(GenreModel.name == name))

    return result.scalars().first()


async def add_book_authors(db: AsyncSession, book_sch: BookScheme, authors: list[str]):
    book = await search_book(db, book_sch)

    for author in authors:
        author_book = await search_author(db, author)
        if not author_book:
            continue
        async with db as session:
            book_author = BookAuthorModel(id_book=book.id, id_author=author_book.id)
            session.add(book_author)
            await session.commit()
            await session.refresh(book_author)


async def add_book_themes(db: AsyncSession, book_sch: BookScheme, themes: list[str]):
    book = await search_book(db, book_sch)

    for theme in themes:
        theme_book = await search_theme(db, theme)
        if not theme_book:
            continue
        async with db as session:
            book_theme = BookThemeModel(id_book=book.id, id_theme=theme_book.id)
            session.add(book_theme)
            await session.commit()
            await session.refresh(book_theme)


async def add_book_genres(db: AsyncSession, book_sch: BookScheme, genres: list[str]):
    book = await search_book(db, book_sch)

    for genre in genres:
        genre_book = await search_genre(db, genre)
        if not genre_book:
            continue
        async with db as session:
            book_genre = BookGenreModel(id_book=book.id, id_genre=genre_book.id)
            session.add(book_genre)
            await session.commit()
            await session.refresh(book_genre)


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

    async with db as session:
        query = await session.execute(select(BookModel).offset(offset).limit(page_size))

    books = query.scalars().all()

    return books
