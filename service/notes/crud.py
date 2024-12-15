from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func, and_

from auth.models import UsersModel
from books.models import BookModel
from notes.models import CheckpointModel, NoteModel


async def new_checkpoint(
    db: AsyncSession, book: BookModel, user: UsersModel, page: int
) -> bool:

    await db.merge(book)
    await db.merge(user)

    checkpoint = await db.execute(
        select(CheckpointModel).filter(
            and_(CheckpointModel.id_book == book.id, CheckpointModel.id_user == user.id)
        )
    )

    checkpoint = checkpoint.scalars().first()

    if not checkpoint:
        checkpoint = CheckpointModel(id_user=user.id, id_book=book.id, page=page)
        db.add(checkpoint)
        await db.commit()

        return True

    checkpoint.page = page
    db.add(checkpoint)
    await db.commit()

    return True


async def show_checkpoint(db: AsyncSession, book: BookModel, user: UsersModel) -> int:

    await db.merge(book)
    await db.merge(user)

    checkpoint = await db.execute(
        select(CheckpointModel).filter(
            and_(CheckpointModel.id_book == book.id, CheckpointModel.id_user == user.id)
        )
    )

    checkpoint = checkpoint.scalars().first()

    if not checkpoint:
        return 0

    return checkpoint.page


async def search_note(
    db: AsyncSession, book: BookModel, user: UsersModel, page: int, description: str
) -> NoteModel:
    await db.merge(book)
    await db.merge(user)

    note = await db.execute(
        select(NoteModel).filter(
            and_(
                NoteModel.id_user == user.id,
                NoteModel.id_book == book.id,
                NoteModel.page == page,
                NoteModel.description == description,
            )
        )
    )

    return note.scalars().first()


async def add_note(
    db: AsyncSession, book: BookModel, user: UsersModel, page: int, description: str
) -> bool:
    await db.merge(book)
    await db.merge(user)

    note = await search_note(db, book, user, page, description)

    if note:
        return False

    note = NoteModel(
        id_user=user.id, id_book=book.id, page=page, description=description
    )

    db.add(note)
    await db.commit()

    return True


async def update_note(
    db: AsyncSession,
    book: BookModel,
    user: UsersModel,
    page: int,
    description: str,
    new_description: str,
) -> bool:
    note = await search_note(db, book, user, page, description)

    if not note:
        return False

    note.description = new_description

    db.add(note)
    await db.commit()

    return True


async def delete_note(
    db: AsyncSession, book: BookModel, user: UsersModel, page: int, description: str
):
    note = await search_note(db, book, user, page, description)

    if not note:
        return False

    await db.delete(note)
    await db.commit()

    return True


async def show_notes(db: AsyncSession, book: BookModel, user: UsersModel):

    await db.merge(book)
    await db.merge(user)

    notes = await db.execute(
        select(NoteModel)
        .filter(and_(NoteModel.id_user == user.id, NoteModel.id_book == book.id))
        .order_by(NoteModel.page)
    )

    return notes.scalars().all()
