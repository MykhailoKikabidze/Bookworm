from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
    File,
    UploadFile,
    Form,
)
from fastapi.middleware.cors import CORSMiddleware

import auth.schemas
from books.models import BookModel
from db import AsyncSessionLocal
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import StreamingResponse
from jose import jwt, JWTError
from datetime import datetime, timedelta
from auth.crud import get_user, authenticate_user, authorize_user
from notes.schemas import NoteSchema
from setting.crud import change_username, change_password, delete_account
from auth import schemas, models
from books.schemas import BookScheme, AuthorScheme
from books.crud import (
    add_book,
    search_book_by_title,
    get_books_paginated,
    get_authors_substr,
    get_authors_of_book,
    get_genres_of_book,
    get_themes_of_book,
    add_author,
    delete_book,
)
from notes.crud import (
    new_checkpoint,
    show_checkpoint,
    add_note,
    update_note,
    delete_note,
    show_notes,
)
import uvicorn
import asyncio
import json
import typing
import os
import io
from minio import Minio, S3Error


app = FastAPI()

settings_path = os.path.join(os.path.dirname(__file__), "settings.json")

with open(settings_path, "r") as file:
    data = json.load(file)

SECRET_KEY = data["SECRET_KEY"]
ALGORITHM = data["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = data["ACCESS_TOKEN_EXPIRE_MINUTES"]
MINIO_HOST = os.getenv("MINIO_HOST", "localhost")
MINIO_PORT = os.getenv("MINIO_PORT", "9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "your_access_key")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "your_secret_key")
BUCKET_NAME_BOOKS = "books"
BUCKET_NAME_IMG_BOOKS = "books-img"


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition", "Location"],
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


minio_client = Minio(
    f"{MINIO_HOST}:{MINIO_PORT}",
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False,
)

if not minio_client.bucket_exists(BUCKET_NAME_BOOKS):
    minio_client.make_bucket(BUCKET_NAME_BOOKS)

if not minio_client.bucket_exists(BUCKET_NAME_IMG_BOOKS):
    minio_client.make_bucket(BUCKET_NAME_IMG_BOOKS)


async def run_server() -> None:
    config = uvicorn.Config("api:app", host="0.0.0.0", port=8000)
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


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db_session)
) -> models.UsersModel:
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
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db_session),
):
    user = await authenticate_user(db, form_data.username, form_data.password)

    if not user:
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
    user = schemas.UsersScheme(
        name=curr_user.name, login=curr_user.login, is_moder=curr_user.is_moder
    )
    return user


@app.post("/users", tags=["logging"], response_model=typing.Dict)
async def create_user(
    user: schemas.UsersScheme, db: AsyncSession = Depends(get_db_session)
):
    result = await authorize_user(db, user)

    if isinstance(result, auth.schemas.UserError):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=result.message,
        )
    return {"status": 200}


@app.put("/users/name", tags=["settings"], response_model=typing.Dict)
async def update_username(
    new_username: str,
    curr_user: models.UsersModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    if curr_user:
        await change_username(db, curr_user, new_username)
        return {"status": 200}
    return {"status": 404}


@app.put("/users/password", tags=["settings"], response_model=typing.Dict)
async def update_password(
    new_password: str,
    curr_user: models.UsersModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    if curr_user:
        await change_password(db, curr_user, new_password)
        return {"status": 200}
    return {"status": 404}


@app.delete("/users", tags=["settings"], response_model=typing.Dict)
async def delete_user(
    curr_user: models.UsersModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    await delete_account(db, curr_user)
    return {"status": 200}


@app.post("/books/", tags=["moderation"], response_model=dict)
async def add_book_full(
    book_sch: BookScheme = Depends(),
    authors: str = Form(...),
    themes: str = Form(...),
    genres: str = Form(...),
    file_img_book: UploadFile = File(...),
    file_book: UploadFile = File(...),
    curr_user: models.UsersModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    if not curr_user.is_moder:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not a moderator",
        )

    authors = authors.split(",")
    themes = themes.split(",")
    genres = genres.split(",")

    try:
        file_image_content = await file_img_book.read()
        file_book_content = await file_book.read()

        if len(file_image_content) == 0 or len(file_book_content) == 0:
            raise HTTPException(status_code=400, detail="One or both files are empty.")

        file_book_stream = io.BytesIO(file_book_content)
        file_image_stream = io.BytesIO(file_image_content)

        file_name_image = book_sch.title + "_IMG"
        file_name_book = book_sch.title

        if not minio_client.bucket_exists(BUCKET_NAME_BOOKS):
            minio_client.make_bucket(BUCKET_NAME_BOOKS)

        if not minio_client.bucket_exists(BUCKET_NAME_IMG_BOOKS):
            minio_client.make_bucket(BUCKET_NAME_IMG_BOOKS)

        minio_client.put_object(
            bucket_name=BUCKET_NAME_BOOKS,
            object_name=file_name_book,
            data=file_book_stream,
            length=len(file_book_content),
            content_type=file_book.content_type,
        )
        file_book_url = (
            f"http://{MINIO_HOST}:{MINIO_PORT}/{BUCKET_NAME_BOOKS}/{file_name_book}"
        )

        minio_client.put_object(
            bucket_name=BUCKET_NAME_IMG_BOOKS,
            object_name=file_name_image,
            data=file_image_stream,
            length=len(file_image_content),
            content_type=file_img_book.content_type,
        )
        file_img_url = f"http://{MINIO_HOST}:{MINIO_PORT}/{BUCKET_NAME_IMG_BOOKS}/{file_name_image}"

    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"Exception MinIO: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cannot load file: {str(e)}")

    load_book_sch = book_sch.model_copy()
    load_book_sch.url = file_book_url
    load_book_sch.url_img = file_img_url

    res = await add_book(db, load_book_sch, authors, themes, genres)

    if not res:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Book already exists",
        )

    return {"status": 200}


@app.get("/books/file", tags=["library"])
async def get_book_file(title: str, db: AsyncSession = Depends(get_db_session)):
    book: BookModel = await search_book_by_title(db, title)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book doesn't exists",
        )
    url: str = book.url
    file_name: str = url.split("/")[-1]

    try:

        response = minio_client.get_object(BUCKET_NAME_BOOKS, file_name)

        return StreamingResponse(
            response,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={file_name}"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"File not found: {str(e)}"
        )


@app.get("/books/img", tags=["library"])
async def get_book_img(title: str, db: AsyncSession = Depends(get_db_session)):
    book: BookModel = await search_book_by_title(db, title)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book doesn't exists",
        )
    url_img: str = book.url_img
    file_name: str = url_img.split("/")[-1]

    try:

        response = minio_client.get_object(BUCKET_NAME_IMG_BOOKS, file_name)

        return StreamingResponse(
            response,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={file_name}"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"File not found: {str(e)}"
        )


@app.get("/books/info", tags=["library"], response_model=BookScheme)
async def get_book_info(title: str, db: AsyncSession = Depends(get_db_session)):
    book: BookModel = await search_book_by_title(db, title)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book doesn't exists",
        )
    book_sch: BookScheme = BookScheme(
        title=book.title,
        year_of_pub=book.year_of_pub,
        url=book.url,
        url_img=book.url_img,
        num_of_pages=book.num_of_pages,
        description=book.description,
        publisher=book.publisher,
    )

    return book_sch


@app.get("/books/all", tags=["library"], response_model=list[BookScheme])
async def get_book_all(
    page: int, page_size: int, db: AsyncSession = Depends(get_db_session)
):
    books: list[BookModel] = await get_books_paginated(db, page, page_size)
    return books


@app.get("/author/substr", tags=["moderation"], response_model=list[AuthorScheme])
async def search_authors_by_substr(
    substr: str, db: AsyncSession = Depends(get_db_session)
):
    res = await get_authors_substr(db, substr.lower())
    return res


@app.get("/books/authors", tags=["library"], response_model=list[AuthorScheme])
async def authors_of_book(title: str, db: AsyncSession = Depends(get_db_session)):
    result = await get_authors_of_book(db, title)
    return result


@app.get("/books/genres", tags=["library"], response_model=list[str])
async def genres_of_book(title: str, db: AsyncSession = Depends(get_db_session)):
    result = await get_genres_of_book(db, title)
    return result


@app.get("/books/themes", tags=["library"], response_model=list[str])
async def themes_of_book(title: str, db: AsyncSession = Depends(get_db_session)):
    result = await get_themes_of_book(db, title)
    return result


@app.post("/authors", tags=["moderation"], response_model=dict)
async def add_authors(
    name: str,
    surname: str,
    db: AsyncSession = Depends(get_db_session),
    curr_user: models.UsersModel = Depends(get_current_user),
):
    if not curr_user.is_moder:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not a moderator",
        )

    res = await add_author(db, name, surname)
    if res:
        return {"status": 200}

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="This author already exists",
    )


@app.delete("/books", tags=["moderation"], response_model=dict)
async def remove_book(
    title: str,
    db: AsyncSession = Depends(get_db_session),
    curr_user: models.UsersModel = Depends(get_current_user),
):
    if not curr_user.is_moder:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not a moderator",
        )

    res = await delete_book(db, title)
    if res:
        return {"status": 200}

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="This author already exists",
    )


@app.post("/checkpoints", tags=["notes"], response_model=dict)
async def add_checkpoint(
    title: str,
    page: int,
    db: AsyncSession = Depends(get_db_session),
    curr_user: models.UsersModel = Depends(get_current_user),
):
    book = await search_book_by_title(db, title)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book is not founded"
        )
    res = await new_checkpoint(db, book, curr_user, page)
    if res:
        return {"status": 200}
    return {"status": 400}


@app.get("/checkpoints", tags=["notes"], response_model=int)
async def get_checkpoint(
    title: str,
    db: AsyncSession = Depends(get_db_session),
    curr_user: models.UsersModel = Depends(get_current_user),
):
    book = await search_book_by_title(db, title)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book is not founded"
        )
    res = await show_checkpoint(db, book, curr_user)
    return res


@app.get("/notes", tags=["notes"], response_model=list[NoteSchema])
async def get_notes(
    title: str,
    db: AsyncSession = Depends(get_db_session),
    curr_user: models.UsersModel = Depends(get_current_user),
):
    book = await search_book_by_title(db, title)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book is not founded"
        )
    res = await show_notes(db, book, curr_user)
    return res


@app.post("/notes", tags=["notes"], response_model=dict)
async def create_note(
    title: str,
    page: int,
    description: str,
    db: AsyncSession = Depends(get_db_session),
    curr_user: models.UsersModel = Depends(get_current_user),
):
    book = await search_book_by_title(db, title)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book is not founded"
        )

    await add_note(db, book, curr_user, page, description)

    return {"status": 200}


@app.put("/notes", tags=["notes"], response_model=dict)
async def change_note(
    title: str,
    page: int,
    description: str,
    new_description: str,
    db: AsyncSession = Depends(get_db_session),
    curr_user: models.UsersModel = Depends(get_current_user),
):
    book = await search_book_by_title(db, title)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book is not founded"
        )

    res = await update_note(db, book, curr_user, page, description, new_description)

    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note is not found"
        )

    return {"status": 200}


@app.delete("/notes", tags=["notes"], response_model=dict)
async def remove_note(
    title: str,
    page: int,
    description: str,
    db: AsyncSession = Depends(get_db_session),
    curr_user: models.UsersModel = Depends(get_current_user),
):
    book = await search_book_by_title(db, title)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book is not founded"
        )

    res = await delete_note(db, book, curr_user, page, description)

    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note is not found"
        )

    return {"status": 200}
