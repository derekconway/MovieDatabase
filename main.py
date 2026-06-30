import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# ==================================================
# 1. DATABASE SETUP
# ==================================================
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

# =================================================
# 2. GUI APPLICATION CLASS
# =================================================
class MovieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My Movie Database")
        self.root.geometry("800x450")

        # UI Input Variables
        self.var_id_num = tk.StringVar()
        self.var_title = tk.StringVar()
        self.var_director = tk.StringVar()
        self.var_year = tk.StringVar()
        self.var_genre = tk.StringVar()

        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        """Layout definitions for inputs, buttons, and the database table view."""
        #--- Form Frame (Left Side)---
        form_frame = ttk.LabelFrame(self.root, text=" Movie Details ", padding=15)
        form_frame.place(x=20, y=20, width=280, height=390)

        ttk.Label(form_frame, text="ID Number:").grid(row=0, column=0, sticky='w', pady=5)
        ttk.Entry(form_frame, textvariable=self.var_id_num, width=25, state="readonly").grid(row=0, column=1, pady=5)

        ttk.Label(form_frame, text="Title:").grid(row=1, column=0, sticky='w', pady=5)
        ttk.Entry(form_frame, textvariable=self.var_title, width=25,).grid(row=1, column=1, pady=5)

        ttk.Label(form_frame, text="Director:").grid(row=2, column=0, sticky='w', pady=5)
        ttk.Entry(form_frame, textvariable=self.var_director, width=25, ).grid(row=2, column=1, pady=5)

        ttk.Label(form_frame, text="Year:").grid(row=3, column=0, sticky='w', pady=5)
        ttk.Entry(form_frame, textvariable=self.var_year, width=25, ).grid(row=3, column=1, pady=5)

        ttk.Label(form_frame, text="Genre:").grid(row=4, column=0, sticky='w', pady=5)
        ttk.Entry(form_frame, textvariable=self.var_genre, width=25, ).grid(row=4, column=1, pady=5)

        # Action Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)

        ttk.Button(btn_frame, text="Add Movie", command=self.add_movie).grid(row=5, column=0, pady=4)
        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_movie).grid(row=6, column=0, pady=4)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_entries).grid(row=7, column=1, pady=4)
        ttk.Button(btn_frame, text="Search Database", command=self.search_database).grid(row=5, column=1, pady=4)
        ttk.Button(btn_frame, text="Reset Search", command=self.reset_search).grid(row=6, column=1, pady=4)

        # --- Tabel Frame (Right Side) ---
        table_frame = ttk.Frame(self.root)
        table_frame.place(x=320, y=25, width=460, height=385)

        # Treeview Scrollbar
        scrolly = ttk.Scrollbar(table_frame, orient="vertical")

        # Movie Table Configuration
        self.movie_table = ttk.Treeview(
            table_frame,
            columns=("id", "title", "director", "year", "genre"),
            show="headings",
            yscrollcommand=scrolly.set
        )
        scrolly.config(command=self.movie_table.yview)
        scrolly.pack(side="right", fill="y")

        # Column Headings
        self.movie_table.heading("id", text="ID")
        self.movie_table.heading("title", text="Title")
        self.movie_table.heading("director", text="Director")
        self.movie_table.heading("year", text="Year")
        self.movie_table.heading("genre", text="Genre")

        self.movie_table.column("id", width=30, anchor="center")
        self.movie_table.column("title", width=140)
        self.movie_table.column("director", width=110)
        self.movie_table.column("year", width=50, anchor="center")
        self.movie_table.column("genre", width=90)

        self.movie_table.pack(fill="both", expand=True)
        self.movie_table.bind("<<TreeviewSelect>>", self.get_cursor_row)

    # ===========================================
    # 3. CORE DATABASE OPERATIONS (CRUD)
    # ===========================================
    def refresh_table(self):
        """Fetches items from database and builds the visual list rows."""
        self.movie_table.delete(*self.movie_table.get_children())
        conn = sqlite3.connect("movies.db")
        cursor = conn.cursor()
        cursor.execute("Select * FROM movies")
        rows = cursor.fetchall()
        for row in rows:
            self.movie_table.insert("", "end", values=row)

        conn.close()

    def add_movie(self):
        """Validates entry fields and saves a row to SQLite database"""
        if not self.var_title.get():
            messagebox.showerror("Error", "The movie Title field is required.")
            return

        year = self.var_year.get()

        if year:
            try:
                year = int(year)
            except ValueError:
                messagebox.showerror("Error", "Year must be a number.")
                return

        conn = sqlite3.connect("movies.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO movies (title, director, year, genre) VALUES (?, ?, ?, ?)",
            (self.var_title.get(), self.var_director.get(), year, self.var_genre.get())

        )
        conn.commit()
        conn.close()

        self.refresh_table()
        self.clear_entries()
        messagebox.showinfo("Success", "Movie added to database successfully!")

    def delete_movie(self):
        """Removes the highlighted table item directly from the database record."""
        selected_item = self.movie_table.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a movie row to delete.")
            return

        content = self.movie_table.item(selected_item)
        row_id = content["values"][0] # Extract DB ID

        conn = sqlite3.connect("movies.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM movies WHERE id = ?", (row_id,))
        conn.commit()
        conn.close()

        confirm = messagebox.askyesno("Confirm Delete", "Delete this movie?")
        if not confirm:
            return

        self.refresh_table()
        self.clear_entries()

    def get_cursor_row(self, event):
        """Fills entry boxes instantly when clicking a row in the table."""
        cursor_row = self.movie_table.focus()
        contents = self.movie_table.item(cursor_row)
        row = contents.get("values")
        if row:
            self.var_id_num.set(row[0])
            self.var_title.set(row[1])
            self.var_director.set(row[2])
            self.var_year.set(row[3])
            self.var_genre.set(row[4])

    def clear_entries(self):
        """Resets the data inputs on the form screen"""
        self.var_id_num.set("")
        self.var_title.set("")
        self.var_director.set("")
        self.var_year.set("")
        self.var_genre.set("")

    def search_database(self):
        if not self.var_title.get():
            messagebox.showerror("Error", "The Movie Title field is required to search.")
            return

        try:
            conn = sqlite3.connect("movies.db")
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM movies WHERE title LIKE ?", ('%' + self.var_title.get() + '%',))
            result = cursor.fetchall()
            conn.close()

            if result:
                self.movie_table.delete(*self.movie_table.get_children())

                for row in result:
                    self.movie_table.insert("", "end", values=row)

            else:
                messagebox.showerror("Error", "The movie is not in the database.")
                self.clear_entries()

        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def reset_search(self):
        self.clear_entries()
        self.refresh_table()


# ===========================================
# 4. EXECUTION
# ===========================================
if __name__ == "__main__":
    init_db() # Verify backend file exists
    root = tk.Tk()
    app = MovieApp(root)
    root.mainloop()




















