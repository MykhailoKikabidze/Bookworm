from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from db import AsyncSessionLocal
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta
from auth.crud import get_user, authenticate_user, authorize_user
from auth import schemas, models
import uvicorn
import asyncio
import json


app = FastAPI()


with open(r'C:\Users\HP\MYFILES\Progs\Bookworm\service\settings.json', 'r') as file:
    data = json.load(file)

SECRET_KEY = data["SECRET_KEY"]
ALGORITHM = data["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = data["ACCESS_TOKEN_EXPIRE_MINUTES"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)


@app.get("/")
async def root():
    return {"connection": True}


async def get_db_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


async def run_server():
    config = uvicorn.Config("api:app", host="127.0.0.1", port=8000, reload=True)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(run_server())


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(info: dict, expires_delta: timedelta = None):
    to_encode = info.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db_session)):
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
    return schemas.UsersScheme(name=user.name, login=user.login, is_moder=user.is_moder)


@app.post("/token")
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


@app.get("/users/me")
async def read_users_me(current_user: models.UsersModel = Depends(get_current_user)):
    return current_user


@app.post("/po/users/")
async def create_user(user: schemas.UsersScheme, db: AsyncSession = Depends(get_db_session)):
    result = await authorize_user(db, user)
    if isinstance(result, schemas.UserError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result.get_msg(),
        )
    return {"status": True}

