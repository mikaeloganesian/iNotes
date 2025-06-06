from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSizePolicy

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("sidebar")

        self.setFixedWidth(200)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)


        self.backgroundDiv = QWidget()

        bg_layout = QVBoxLayout()
        self.backgroundDiv.setLayout(bg_layout)
        bg_layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background-color: #64032E;")


        self.icon = QLabel()
        self.icon.setStyleSheet("margin-bottom: 60px;")
        self.icon.setPixmap(QPixmap("resources/images/image.png"))
        # Кнопки меню
        self.notes_button = QPushButton("My SmartNotes")
        self.notes_button.setStyleSheet("background-color: #500A1A; color: white; padding: 14px; text-align: center; text-align: left; margin-bottom: 10px; border-right: 2px solid white;")
        self.notes_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.notes_button.setContentsMargins(0, 0, 0, 0)
        self.kanban_button = QPushButton("Kanban board")
        self.kanban_button.setStyleSheet("background-color: #500A1A; color: white; padding: 14px; text-align: center; text-align: left;  margin-bottom: 10px; border-right: 2px solid white;")
        self.kanban_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.kanban_button.setContentsMargins(0, 0, 0, 0)
        self.settings_button = QPushButton("Settings")
        self.settings_button.setStyleSheet("background-color: #500A1A; color: white; padding: 14px; text-align: center; text-align: left;  margin-bottom: 10px; border-right: 2px solid white;")
        self.settings_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.settings_button.setContentsMargins(0, 0, 0, 0)

        bg_layout.addWidget(self.icon, alignment=Qt.AlignmentFlag.AlignCenter)
        bg_layout.addWidget(self.notes_button)
        bg_layout.addWidget(self.kanban_button)
        bg_layout.addWidget(self.settings_button)
        bg_layout.addStretch()

        layout.addWidget(self.backgroundDiv)

