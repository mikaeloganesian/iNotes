from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton


class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(200)
        self.setStyleSheet("""
            background-color: #202020;
            border-right: 1px solid #2c2c2c;
        """)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Кнопки меню
        self.notes_button = QPushButton("Заметки")
        self.kanban_button = QPushButton("Kanban")
        self.settings_button = QPushButton("Настройки")

        layout.addWidget(self.notes_button)
        layout.addWidget(self.kanban_button)
        layout.addWidget(self.settings_button)
        layout.addStretch()
