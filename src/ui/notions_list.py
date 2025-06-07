# ui/notes_page.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSizePolicy, QScrollArea, QGridLayout, QPushButton, QGraphicsBlurEffect
from PyQt6.QtCore import Qt
from db.db import NotesDB
from ui.editor import MarkdownEditor
from ui.note_card import NoteCard

class NotesPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        # Window label
        header = QLabel("My SmartNotes")
        header.setStyleSheet("font-size: 16px; font-weight: 300; background-color: #500A1A;  color: #ffffff; padding: 20px 10px;")
        layout.addWidget(header)
        layout.addSpacing(20)

        # Прокручиваемая область
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background-color: transparent; border: none;")
        self.content_layout = QGridLayout(self.content_widget)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setSpacing(20)

        # Инициализация базы данных
        self.db = NotesDB()

        # Загружаем заметки
        self.load_notes()

        # !!! ВАЖНО: прикрепляем виджет с контентом к scroll
        scroll.setWidget(self.content_widget)

        # Добавляем scroll в основной layout
        layout.addWidget(scroll)

        self.setLayout(layout)

        self.create_button = QPushButton("Write new notion", self)
        self.create_button.setStyleSheet("background-color: #64032E; color: white; border-radius: 12px; text-align: center;")
        self.create_button.setFixedSize(180, 40)
        self.create_button.raise_()  # Поднимает кнопку поверх всего
        self.create_button.clicked.connect(self.create_new_note)

        self.update_button_position()
    
    def open_note_in_editor(self, note_id, title, content):
        self.editor_window = MarkdownEditor(note_id, title, content, self.db, on_close=self.load_notes)
        self.editor_window.setWindowTitle(title)
        self.editor_window.editor.setPlainText(content)
        self.editor_window.show()
        
    def load_notes(self):
        # Очистка layout
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            widget = item.widget() # type: ignore
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

        notes = self.db.get_all_notes()

        if not notes:
                self.db.add_note("Добро пожаловать!", "Создайте свою первую заметку в iNotes.", "2025-06-01")
                self.db.add_note("Совет", "Нажмите 'Write new notion', чтобы начать.", "2025-06-01")
                self.db.add_note("Подсказка", "Все заметки сохраняются автоматически.", "2025-06-01")
                notes = self.db.get_all_notes()

        for index, note in enumerate(notes):
            note_id, title, date, preview = note
            card = NoteCard(note_id, title, date, preview, self.open_note_in_editor)
            row = index // 3
            col = index % 3
            self.content_layout.addWidget(card, row, col, alignment=Qt.AlignmentFlag.AlignLeft)

        height = self.calculate_content_height(len(notes))
        self.content_widget.setFixedHeight(height)

    def calculate_content_height(self, note_count):
        rows = (note_count + 2) // 3  # по 3 в строку
        card_height = 120
        vertical_spacing = self.content_layout.verticalSpacing() or 0
        margins = self.content_layout.contentsMargins().top() + self.content_layout.contentsMargins().bottom()
        return rows * card_height + (rows - 1) * vertical_spacing + margins


    def create_new_note(self):
        self.db.add_note("Title", "Tap to the note to change it.", "2025-06-01")
        self.load_notes()

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