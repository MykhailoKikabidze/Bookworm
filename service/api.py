from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI
from db import AsyncSessionLocal
import uvicorn
import asyncio


app = FastAPI()


@app.get("/")
async def root():
    return {"connection": True}


async def get_db_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


async def run_server():
    config = uvicorn.Config("api:app", host="0.0.0.0", port=8000, reload=True)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(run_server())
