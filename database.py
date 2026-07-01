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

def delete_movie_from_db(movie_id):
    """Deletes a movie from the database by ID."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
    conn.commit()
    conn.close()

def search_movies_by_title(title):
    """Returns movies that match the title search."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM movies WHERE title LIKE ?", ('%' + title + '%',))
    results = cursor.fetchall()
    conn.close()
    return results