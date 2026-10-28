from contextlib import asynccontextmanager
from datetime import datetime

import psycopg
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

import database
import business_logic


@asynccontextmanager
async def lifespan(_: FastAPI):
    database.initialize()
    yield


app = FastAPI(lifespan=lifespan)


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class ItemResponse(BaseModel):
    id: int
    name: str
    created_at: datetime


@app.get("/")
def read_root():
    return {"ok": True}


@app.get("/health")
def read_health():
    try:
        database.check_connection()
    except psycopg.Error as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database is unavailable",
        ) from error
    return {"status": "healthy", "database": "connected"}


@app.get("/items", response_model=list[ItemResponse])
def list_items():
    return business_logic.list_items()


@app.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate):
    try:
        return business_logic.create_item(item.name)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(error),
        ) from error
