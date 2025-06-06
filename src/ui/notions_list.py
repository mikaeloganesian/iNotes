# ui/notes_page.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSizePolicy, QScrollArea, QGridLayout, QPushButton
from PyQt6.QtCore import Qt
from db.db import NotesDB

class NotesPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # Строка с заметками
        header = QLabel("My SmartNotes")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff;")
        layout.addWidget(header)
        layout.addSpacing(10)

        # Прокручиваемая область
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content_widget = QWidget()
        content_layout = QGridLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(10)

        # Инициализация базы данных
        self.db = NotesDB()
        notes = self.db.get_all_notes()

        if not notes:
            # Если нет заметок, показываем заглушку
            self.db.add_note("Добро пожаловать!", "Создайте свою первую заметку.", "2025-06-01")
            notes = self.db.get_all_notes()

        for index, note in enumerate(notes):
            card = self.create_note_row(note[0], note[1], note[2])
            row = index // 3
            col = index % 3
            content_layout.addWidget(card, row, col, alignment=Qt.AlignmentFlag.AlignLeft)

        height = content_widget.sizeHint().height()
        content_widget.setFixedHeight(height)

        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
        self.setLayout(layout)

        self.create_button = QPushButton("Write new notion", self)
        self.create_button.setStyleSheet("background-color: #64032E; color: white; padding: 10px; border-radius: 6px; text-align: center;")
        self.create_button.setFixedSize(150, 40)
        self.create_button.raise_()  # Поднимает кнопку поверх всего

        self.update_button_position()

    def create_note_row(self, title: str, date: str, preview: str) -> QWidget:
        card = QWidget()
        card.setFixedWidth(222)
        card.setFixedHeight(120)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: 400; font-size: 12px; color: #ffffff;")
        title_label.setWordWrap(True)

        date_label = QLabel(date)
        date_label.setStyleSheet("color: #fff; font-size: 10px;")
        date_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        preview_label = QLabel(preview)
        preview_label.setStyleSheet("color: #fff; font-size: 10px;")
        preview_label.setWordWrap(True)

        layout.addWidget(title_label)
        layout.addWidget(date_label)
        layout.addWidget(preview_label)

        card.setLayout(layout)
        card.setStyleSheet("""
            background-color: #2b2b2b;
            border-radius: 4px;
        """)
                           
        return card
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_button_position()

    def update_button_position(self):
        margin = 20
        x = self.width() - self.create_button.width() - margin
        y = self.height() - self.create_button.height() - margin
        self.create_button.move(x, y)
    
    
    def closeEvent(self, event):
        self.db.close()
        super().closeEvent(event)