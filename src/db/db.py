import sqlite3
from datetime import datetime
from typing import Optional, Tuple, List

class NotesDB:
    def __init__(self, db_path: str = "db/notes.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self) -> None:
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

    def add_note(self, title: str, preview: str, date: Optional[str] = None) -> int | None:
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        query = "INSERT INTO notes (title, date, preview) VALUES (?, ?, ?)"
        cursor = self.conn.execute(query, (title, date, preview))
        self.conn.commit()
        return cursor.lastrowid

    def get_all_notes(self) -> List[Tuple[int, str, str, str]]:
        query = "SELECT id, title, date, preview FROM notes ORDER BY date DESC"
        cursor = self.conn.execute(query)
        return cursor.fetchall()[::-1] # Возвращаем в обратном порядке (от новых к старым)

    def update_note(self,
                    note_id: int,
                    title: Optional[str] = None,
                    preview: Optional[str] = None,
                    date: Optional[str] = None) -> None:
        # Собираем поля для обновления
        fields = []
        values: List[str] = []
        if title is not None:
            fields.append("title = ?")
            values.append(title)
        if preview is not None:
            fields.append("preview = ?")
            values.append(preview)
        if date is not None:
            fields.append("date = ?")
            values.append(date)
        if not fields:
            return  # Нечего обновлять

        query = f"UPDATE notes SET {', '.join(fields)} WHERE id = ?"
        values.append(str(note_id))
        self.conn.execute(query, tuple(values))
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()
