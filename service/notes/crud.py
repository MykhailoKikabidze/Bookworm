from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from auth.models import UsersModel
from books.models import BookModel
from notes.models import CheckpointModel, NoteModel, GroupModel
from notes.schemas import GroupSchema


async def new_checkpoint(
    db: AsyncSession, book: BookModel, user: UsersModel, cfi: str
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
        checkpoint = CheckpointModel(id_user=user.id, id_book=book.id, cfi=cfi)
        db.add(checkpoint)
        await db.commit()

        return True

    checkpoint.cfi = cfi
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

    return checkpoint.cfi


async def search_note(
    db: AsyncSession,
    book: BookModel,
    user: UsersModel,
    page: int,
    description: str,
    quote: str,
    character: str,
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
                NoteModel.quote == quote,
                NoteModel.character == character,
            )
        )
    )

    return note.scalars().first()


async def add_note(
    db: AsyncSession,
    book: BookModel,
    user: UsersModel,
    page: int,
    description: str,
    quote: str,
    character: str,
) -> bool:
    await db.merge(book)
    await db.merge(user)

    note = await search_note(db, book, user, page, description, quote, character)

    if note:
        return False

    note = NoteModel(
        id_user=user.id,
        id_book=book.id,
        page=page,
        description=description,
        quote=quote,
        character=character,
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
    quote: str,
    character: str,
) -> bool:
    note = await search_note(db, book, user, page, description, quote, character)
    note_check = await search_note(
        db, book, user, page, new_description, quote, character
    )

    if not note:
        return False

    if note_check:
        return False

    note.description = new_description

    db.add(note)
    await db.commit()

    return True


async def delete_note(
    db: AsyncSession,
    book: BookModel,
    user: UsersModel,
    page: int,
    description: str,
    quote: str,
    character: str,
):
    note = await search_note(db, book, user, page, description, quote, character)

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


async def search_group(db: AsyncSession, book: BookModel, user: UsersModel):

    await db.merge(book)
    await db.merge(user)

    group = await db.execute(
        select(GroupModel).filter(
            and_(
                GroupModel.id_user == user.id,
                GroupModel.id_book == book.id,
            )
        )
    )

    return group.scalars().first()


async def new_group(
    db: AsyncSession, group: GroupSchema, book: BookModel, user: UsersModel
) -> bool:

    await db.merge(book)
    await db.merge(user)

    check_group = await search_group(db, book, user)

    if check_group:
        return False

    group_model = GroupModel(
        id_user=user.id,
        id_book=book.id,
        is_favourite=group.is_favourite,
        want_to_read=group.want_to_read,
        now_reading=group.now_reading,
        have_read=group.have_read,
    )

    db.add(group_model)
    await db.commit()

    return True


async def change_group(
    db: AsyncSession, group: GroupSchema, book: BookModel, user: UsersModel
) -> bool:

    await db.merge(book)
    await db.merge(user)

    group_model = await search_group(db, book, user)

    if not group_model:
        return False

    group_model.is_favourite = group.is_favourite
    group_model.want_to_read = group.want_to_read
    group_model.now_reading = group.now_reading
    group_model.have_read = group.have_read

    db.add(group_model)
    await db.commit()

    return True


async def delete_group(db: AsyncSession, book: BookModel, user: UsersModel) -> bool:
    await db.merge(book)
    await db.merge(user)

    group_model = await search_group(db, book, user)

    if not group_model:
        return False

    await db.delete(group_model)
    await db.commit()

    return True
