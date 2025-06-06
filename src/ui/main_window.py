from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton
)
from ui.editor import MarkdownEditor
from ui.sidebar import Sidebar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iNotes — Интеллектуальные заметки")

        # Главное виджет-окно
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Главный горизонтальный layout
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # Левая часть — боковая панель
        self.sidebar = Sidebar()

        # Правая часть — контент (Markdown редактор)
        self.content = MarkdownEditor()

        
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content)
