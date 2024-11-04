from sqlalchemy.ext.asyncio import AsyncSession

import auth.models
import service.auth.models as auth_model
from service.auth.crud import get_password_hash


async def change_username(db: AsyncSession, user: auth_model.UsersModel, new_name: str):
    user.name = new_name
    async with db as session:
        session.add(user)
        await session.commit()


async def change_password(db: AsyncSession, user: auth_model.UsersModel, new_password: str):
    user.password = get_password_hash(new_password)
    async with db as session:
        session.add(user)
        await session.commit()


async def delete_account(db: AsyncSession, user_db: auth.models.UsersModel) -> None:
    await db.delete(user_db)
    await db.commit()
