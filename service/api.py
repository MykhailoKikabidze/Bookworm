from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

import auth.models
from db import AsyncSessionLocal
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta
from auth.crud import get_user, authenticate_user, authorize_user
from setting.crud import change_username, change_password
from auth import schemas, models
import uvicorn
import asyncio
import json
import typing


app = FastAPI()


with open(r'C:\Users\HP\MYFILES\Progs\Bookworm\service\settings.json', 'r') as file:
    data = json.load(file)

SECRET_KEY = data["SECRET_KEY"]
ALGORITHM = data["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = data["ACCESS_TOKEN_EXPIRE_MINUTES"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["default"], response_model=typing.Dict)
async def root():
    return {"connection": True}


async def get_db_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def run_server() -> None:
    config = uvicorn.Config("api:app", host="127.0.0.1", port=8000, reload=True)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(run_server())


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(info: dict, expires_delta: timedelta = None) -> str:
    to_encode = info.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db_session)) -> models.UsersModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user(db, username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/token", tags=["logging"], response_model=typing.Dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db_session)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user or isinstance(user, schemas.UserError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        info={"sub": user.login}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", tags=["logging"], response_model=schemas.UsersScheme)
async def read_users_me(curr_user: models.UsersModel = Depends(get_current_user)):
    user = schemas.UsersScheme(name=curr_user.name, login=curr_user.login, is_moder=curr_user.is_moder)
    return user


@app.post("/users", tags=["logging"], response_model=typing.Dict)
async def create_user(user: schemas.UsersScheme, db: AsyncSession = Depends(get_db_session)):
    result = await authorize_user(db, user)

    if str(result.__class__) == "<class 'service.auth.schemas.UserError'>":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=result.message,
        )
    else:
        return {"status": 200}


@app.put("/users/name", tags=["settings"], response_model=typing.Dict)
async def update_username(new_username: str, curr_user: models.UsersModel = Depends(get_current_user), db: AsyncSession = Depends(get_db_session)):
    if curr_user:
        await change_username(db, curr_user, new_username)
        return {"status": 200}
    return {"status": 404}


@app.put("/users/password", tags=["settings"], response_model=typing.Dict)
async def update_password(new_password: str, curr_user: models.UsersModel = Depends(get_current_user), db: AsyncSession = Depends(get_db_session)):
    if curr_user:
        await change_password(db, curr_user, new_password)
        return {"status": 200}
    return {"status": 404}

