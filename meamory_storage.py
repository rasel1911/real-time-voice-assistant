import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "bondhu_memory.db"
MAX_HISTORY_MESSAGES = 12


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)


def save_memory(memory):
    memory = memory.strip()[:500]
    if not memory:
        return

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO memories (memory) VALUES (?)",
            (memory,)
        )


def get_memories():
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT id, memory FROM memories ORDER BY id DESC LIMIT 20"
        ).fetchall()

    if not rows:
        return "No saved memories yet."

    return "\n".join(
        f"{memory_id}. {memory}" for memory_id, memory in rows
    )


def save_message(role, content):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO conversations (role, content) VALUES (?, ?)",
            (role, content[:6000])
        )


def load_recent_history():
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("""
            SELECT role, content
            FROM conversations
            ORDER BY id DESC
            LIMIT ?
        """, (MAX_HISTORY_MESSAGES,)).fetchall()

    rows.reverse()

    return [
        {"role": role, "content": content}
        for role, content in rows
        if role in ("user", "assistant")
    ]