import sqlite3

def init_db():
    """Connects to SQLite and creates the movies table if it doesn't exist."""
    conn = sqlite3.connect("movies_database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            director TEXT,
            year INTEGER,
            genre TEXT
        )
        """)
    conn.commit()
    conn.close()