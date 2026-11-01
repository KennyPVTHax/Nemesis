import hashlib
import hmac
import secrets
import sqlite3
import sys
import time

from account_store import connect


def initialize():
    with connect() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS owner_link_codes (
                id INTEGER PRIMARY KEY CHECK(id=1),
                code_hash TEXT NOT NULL,
                expires_at INTEGER NOT NULL,
                failures INTEGER NOT NULL DEFAULT 0
            )
        """)


def issue_code():
    initialize()

    with connect() as db:
        db.execute("BEGIN IMMEDIATE")

        owner = db.execute("""
            SELECT telegram_chat_id
            FROM users
            WHERE role='owner'
        """).fetchone()

        if not owner:
            raise RuntimeError("Owner account not found")

        if owner[0] is not None:
            print("Owner already linked.")
            return

        code = "NM-" + secrets.token_urlsafe(24)
        digest = hashlib.sha256(code.encode()).hexdigest()

        db.execute("DELETE FROM owner_link_codes")

        db.execute("""
            INSERT INTO owner_link_codes
            (id, code_hash, expires_at, failures)
            VALUES (1, ?, ?, 0)
        """, (digest, int(time.time()) + 600))

    print()
    print("Send this command to your Telegram bot:")
    print()
    print("/link " + code)
    print()
    print("This code expires in 10 minutes.")
    print("Do not share it publicly.")


def consume_code(chat_id, code):
    initialize()

    if not isinstance(chat_id, int) or chat_id <= 0:
        return "invalid"

    if not isinstance(code, str) or len(code) > 100:
        return "invalid"

    digest = hashlib.sha256(code.encode()).hexdigest()
    now = int(time.time())

    with connect() as db:
        db.execute("BEGIN IMMEDIATE")

        owner = db.execute("""
            SELECT id, telegram_chat_id
            FROM users
            WHERE role='owner'
        """).fetchone()

        if not owner:
            return "unavailable"

        owner_id, linked_chat = owner

        if linked_chat is not None:
            return "already" if linked_chat == chat_id else "unavailable"

        row = db.execute("""
            SELECT code_hash, expires_at, failures
            FROM owner_link_codes
            WHERE id=1
        """).fetchone()

        if not row:
            return "invalid"

        saved_hash, expiry, failures = row

        if now >= expiry or failures >= 5:
            db.execute("DELETE FROM owner_link_codes")
            return "expired"

        if not hmac.compare_digest(digest, saved_hash):
            db.execute("""
                UPDATE owner_link_codes
                SET failures=failures+1
                WHERE id=1
            """)
            return "invalid"

        db.execute("""
            UPDATE users
            SET telegram_chat_id=?
            WHERE id=? AND telegram_chat_id IS NULL
        """, (chat_id, owner_id))

        db.execute("DELETE FROM owner_link_codes")

        return "linked"


def is_owner(chat_id):
    with connect() as db:
        row = db.execute("""
            SELECT 1 FROM users
            WHERE role='owner'
              AND is_active=1
              AND telegram_chat_id=?
        """, (chat_id,)).fetchone()

    return row is not None


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] != "new":
        raise SystemExit("Usage: telegram_link.py new")

    issue_code()
