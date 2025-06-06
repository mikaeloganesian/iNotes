import sqlite3
from datetime import datetime
from typing import Optional

class NotesDB:
    def __init__(self, db_path="db/notes.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            preview TEXT NOT NULL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_note(self, title: str, preview: str, date: Optional[str] = None):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        query = "INSERT INTO notes (title, date, preview) VALUES (?, ?, ?)"
        self.conn.execute(query, (title, date, preview))
        self.conn.commit()

    def get_all_notes(self):
        query = "SELECT title, date, preview FROM notes ORDER BY date DESC"
        cursor = self.conn.execute(query)
        return cursor.fetchall()

    def close(self):
        self.conn.close()
