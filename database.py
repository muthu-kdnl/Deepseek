import os

import psycopg
from psycopg.rows import dict_row


def _connect() -> psycopg.Connection:
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "app_db"),
        user=os.getenv("POSTGRES_USER", "app_user"),
        password=os.getenv("POSTGRES_PASSWORD", "local_dev_password"),
        connect_timeout=3,
        row_factory=dict_row,
    )


def initialize() -> None:
    with _connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
            """
        )


def check_connection() -> None:
    with _connect() as connection:
        connection.execute("SELECT 1")


def list_items() -> list[dict]:
    with _connect() as connection:
        rows = connection.execute(
            "SELECT id, name, created_at FROM items ORDER BY id"
        ).fetchall()
    return list(rows)


def create_item(name: str) -> dict:
    with _connect() as connection:
        row = connection.execute(
            "INSERT INTO items (name) VALUES (%s) RETURNING id, name, created_at",
            (name,),
        ).fetchone()
    return row
