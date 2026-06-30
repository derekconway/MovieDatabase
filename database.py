import sqlite3

DATABASE_NAME = "movies_database.db"

def init_db():
    """Connects to SQLite and creates the movies table if it doesn't exist."""
    conn = sqlite3.connect(DATABASE_NAME)
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

def get_all_movies():
    """Returns all movies from the database."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM movies")

    rows = cursor.fetchall()

    conn.close()
    return rows

def add_movie_to_db(title, director, year, genre):
    """Adds a movie to the database."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO movies (title, director, year, genre) VALUES (?, ?, ?, ?)",
        (title, director, year, genre)
    )
    conn.commit()
    conn.close()