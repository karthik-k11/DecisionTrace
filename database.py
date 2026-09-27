import json
import sqlite3
from datetime import datetime
from pathlib import Path


DATABASE_DIR = Path("database")
DATABASE_PATH = DATABASE_DIR / "decisiontrace.db"


def get_connection():
    DATABASE_DIR.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            decision TEXT NOT NULL,
            input_summary TEXT NOT NULL,
            result_json TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def save_analysis(input_text, result):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO decisions (
            created_at,
            decision,
            input_summary,
            result_json
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            datetime.now().isoformat(timespec="seconds"),
            result.decision,
            input_text[:200],
            json.dumps(result.model_dump()),
        ),
    )

    connection.commit()
    connection.close()