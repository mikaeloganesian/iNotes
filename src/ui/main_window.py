from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton
)
from ui.editor import MarkdownEditor
from ui.sidebar import Sidebar
from ui.notions_list import NotesPage
from PyQt6.QtCore import Qt



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iNotes — Интеллектуальные заметки")
        self.resize(987, 686)

        # Главное виджет-окно
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Главный горизонтальный layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы от краёв
        main_layout.setSpacing(0)  # Убираем промежутки между виджетами
        main_widget.setLayout(main_layout)

        # Левая часть — боковая панель
        self.sidebar = Sidebar()

        # Правая часть — контент (Markdown редактор)
        self.content = NotesPage()
        self.content.setStyleSheet("background-color: #F8F8F8;")  # Устанавливаем цвет фона
        
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content)

        self.sidebar.raise_()


        self.setFixedSize(self.size())
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setMinimumSize(987, 686)
        self.setMaximumSize(987, 686)