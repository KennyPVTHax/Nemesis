import getpass
import os
import sqlite3
import sys
import time
from pathlib import Path

from argon2 import PasswordHasher, Type

DB_PATH = Path("/opt/nemesis/data/accounts.sqlite3")

HASHER = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=2,
    hash_len=32,
    salt_len=16,
    type=Type.ID,
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login_id TEXT NOT NULL UNIQUE COLLATE NOCASE,
    password_hash TEXT NOT NULL,
    telegram_chat_id INTEGER UNIQUE,
    role TEXT NOT NULL CHECK(role IN ('owner', 'user')),
    is_active INTEGER NOT NULL DEFAULT 1
        CHECK(is_active IN (0, 1)),
    created_at INTEGER NOT NULL,
    expires_at INTEGER,
    CHECK(role <> 'owner' OR expires_at IS NULL)
);

CREATE UNIQUE INDEX IF NOT EXISTS one_nemesis_owner
ON users(role) WHERE role='owner';
"""


def connect():
    db = sqlite3.connect(str(DB_PATH), timeout=10)
    db.execute("PRAGMA foreign_keys=ON")
    db.execute("PRAGMA busy_timeout=5000")
    return db


def initialize():
    if DB_PATH.is_symlink():
        raise RuntimeError("Database symlink not allowed")

    if not DB_PATH.parent.is_dir():
        raise RuntimeError("Data directory missing")

    os.umask(0o077)

    with connect() as db:
        db.executescript(SCHEMA)

    os.chmod(DB_PATH, 0o600)


def create_owner():
    with connect() as db:
        existing = db.execute(
            "SELECT 1 FROM users WHERE role='owner'"
        ).fetchone()

    if existing:
        print("Owner already exists; nothing changed.")
        return

    password = getpass.getpass(
        "Create NEW NemesisOwner password (12-256 chars): "
    )
    confirmation = getpass.getpass(
        "Confirm owner password: "
    )

    if password != confirmation:
        raise SystemExit("Passwords do not match.")

    if not 12 <= len(password) <= 256:
        raise SystemExit("Password must contain 12-256 characters.")

    if not password.strip():
        raise SystemExit("Password cannot be only whitespace.")

    hashed = HASHER.hash(password)
    del password, confirmation

    with connect() as db:
        db.execute("BEGIN IMMEDIATE")

        if db.execute(
            "SELECT 1 FROM users WHERE role='owner'"
        ).fetchone():
            raise SystemExit("Owner already exists.")

        db.execute("""
            INSERT INTO users
            (login_id, password_hash, telegram_chat_id,
             role, is_active, created_at, expires_at)
            VALUES (?, ?, NULL, 'owner', 1, ?, NULL)
        """, ("NemesisOwner", hashed, int(time.time())))

    print("OWNER CREATED: NemesisOwner")
    print("PASSWORD HASHING: Argon2id")
    print("TELEGRAM LINKING: PENDING")


def verify():
    with connect() as db:
        row = db.execute("""
            SELECT login_id, role, is_active, expires_at,
                   telegram_chat_id IS NOT NULL,
                   password_hash
            FROM users
            WHERE role='owner'
        """).fetchone()

    if not row:
        print("OWNER: NOT YET CREATED")
        return

    name, role, active, expires, linked, digest = row

    assert role == "owner"
    assert active == 1
    assert expires is None
    assert digest.startswith("$argon2id$")

    print("OWNER:", name)
    print("PASSWORD STORAGE: PASS")
    print("OWNER UNLIMITED ACCESS: PASS")
    print("TELEGRAM LINKED:", bool(linked))
    print("DATABASE VERIFICATION: PASS")


if __name__ == "__main__":
    initialize()

    if len(sys.argv) != 2 or sys.argv[1] not in (
        "create-owner", "verify"
    ):
        raise SystemExit(
            "Usage: account_store.py create-owner|verify"
        )

    if sys.argv[1] == "create-owner":
        create_owner()
    else:
        verify()
