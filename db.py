import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "deals.db"
SCHEMA = Path(__file__).parent / "schema.sql"

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect() as conn:
        conn.executescript(SCHEMA.read_text())
