import sqlite3
from pathlib import Path


DB_Path = Path.home()/'.contact-book'/'contacts.db'


SCHEMA = '''

CREATE TABLE IF NOT EXISTS contacts (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name NOT NULL CHECK(length(trim(name)) > 0 ),
    phone TEXT,
    email TEXT,
    address TEXT,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT (
        strftime('%Y-%m-%dT%H:%M:%fZ','now')
    ),
    updated_at TEXT NOT NULL DEFAULT (
        strftime('%Y-%m-%dT%H:%M:%fZ','now')
    )

 );

'''


def connect():
    DB_Path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_Path, timeout=5)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    conn.execute('PRAGMA busy_timeout = 5000')
    conn.executescript(SCHEMA)

    return conn


connect()