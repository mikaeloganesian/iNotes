# ui/notes_page.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSizePolicy, QScrollArea, QGridLayout, QPushButton
from PyQt6.QtCore import Qt
from db.db import NotesDB

class NotesPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        # Строка с заметками
        header = QLabel("My SmartNotes")
        header.setStyleSheet("font-size: 16px; font-weight: 300; background-color: #500A1A;  color: #ffffff; padding: 20px 10px;")
        layout.addWidget(header)
        layout.addSpacing(10)

        # Прокручиваемая область
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background-color: transparent;")
        self.content_layout = QGridLayout(self.content_widget)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setSpacing(24)

        # Инициализация базы данных
        self.db = NotesDB()

        # Загружаем заметки
        self.load_notes()

        # !!! ВАЖНО: прикрепляем виджет с контентом к scroll
        scroll.setWidget(self.content_widget)

        # Добавляем scroll в основной layout
        layout.addWidget(scroll)

        self.load_notes()
        layout.addWidget(scroll)
        self.setLayout(layout)

        self.create_button = QPushButton("Write new notion", self)
        self.create_button.setStyleSheet("background-color: #64032E; color: white;  border-radius: 12px; text-align: center;")
        self.create_button.setFixedSize(180, 40)
        self.create_button.raise_()  # Поднимает кнопку поверх всего
        self.create_button.clicked.connect(self.create_new_note)

        self.update_button_position()

    def create_note_row(self, title: str, date: str, preview: str) -> QWidget:
        card = QWidget()
        card.setFixedWidth(222)
        card.setFixedHeight(120)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 10)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: 400; font-size: 12px; background-color: #64032E; color: white; border-radius: 0px; padding: 5px;")
        title_label.setWordWrap(True)

        date_label = QLabel(date)
        date_label.setStyleSheet("font-size: 10px; background-color: transparent; padding: 4px;")
        date_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        preview_label = QLabel(preview)
        preview_label.setStyleSheet("font-size: 10px; background-color: transparent; padding: 4px;")
        preview_label.setWordWrap(True)

        layout.addWidget(title_label)
        layout.addWidget(date_label)
        layout.addWidget(preview_label)

        card.setLayout(layout)
        card.setStyleSheet("border-radius: 4px; background: rgba(255, 255, 255, 0.85); color: black;")
                           
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

    def load_notes(self):
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()


        notes = self.db.get_all_notes()

        if not notes:
            self.db.add_note("Добро пожаловать!", "Создайте свою первую заметку.", "2025-06-01")
            self.db.add_note("Совет", "Нажмите 'Write new notion', чтобы начать.", "2025-06-01")
            self.db.add_note("Подсказка", "Все заметки сохраняются автоматически.", "2025-06-01")
            notes = self.db.get_all_notes()

        for index, note in enumerate(notes):
            card = self.create_note_row(note[0], note[1], note[2])
            row = index // 3
            col = index % 3
            self.content_layout.addWidget(card, row, col, alignment=Qt.AlignmentFlag.AlignLeft)

            card_height = 120
            spacing = self.content_layout.spacing()
            margins = self.content_layout.contentsMargins().top() + self.content_layout.contentsMargins().bottom()
            rows = (len(notes) + 2) // 3  # делим на 3, округляя вверх
            total_height = rows * card_height + (rows - 1) * spacing + margins

            self.content_widget.setFixedHeight(total_height)



    def create_new_note(self):
        self.db.add_note("New Note", "This is a new note.", "2025-06-01")
        self.load_notes()