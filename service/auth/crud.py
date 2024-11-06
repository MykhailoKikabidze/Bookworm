from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, Union
from auth import schemas, models


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def get_user(db: AsyncSession, login: str) -> Optional[models.UsersModel]:
    result = await db.execute(
        select(models.UsersModel).filter(models.UsersModel.login == login)
    )
    return result.scalars().first()


async def authenticate_user(
    db: AsyncSession, username: str, password: str
) -> Union[bool, schemas.UserError]:
    user: models.UsersModel | None = await get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def authorize_user(
    db: AsyncSession, user: schemas.UsersScheme
) -> Union[models.UsersModel, schemas.UserError]:
    user_db: models.UsersModel | None = await get_user(db, user.login)
    if user_db:
        return schemas.UserError("User already exists")
    user.password = get_password_hash(user.password)

    user_db = models.UsersModel(
        name=user.name, login=user.login, password=user.password, is_moder=user.is_moder
    )

    async with db as session:
        session.add(user_db)
        await session.commit()
        await session.refresh(user_db)

    return user_db
