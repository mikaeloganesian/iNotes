from PyQt6.QtWidgets import QWidget, QLineEdit, QTextEdit, QTextBrowser, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QCloseEvent
from app.markdown import convert_markdown_to_html
from db.db import NotesDB

class MarkdownEditor(QWidget):
    def __init__(self, note_id: int, title: str, preview: str, db: NotesDB, on_close=None):
        super().__init__()
        self.on_close = on_close
        self.note_id = note_id
        self.db = db

        self.setStyleSheet("background-color: #F8F8F8; font-family: 'Segoe UI'; font-size: 14px; color: #000; border: 3px solid #64032E; border-radius: 4px;")

        self.title_input = QLineEdit()
        self.title_input.setStyleSheet("padding: 10px; font-weight: bold; font-size: 16px; color: #64032E;")
        self.title_input.setText(title)

        self.editor = QTextEdit()
        self.editor.setStyleSheet("padding: 10px;")
        self.editor.setPlainText(preview)

        self.preview = QTextBrowser()
        self.preview.setStyleSheet("padding: 10px; background-color: #64032E; color: white; border: 2px solid #64032E; border-radius: 4px;")

        self.editor.textChanged.connect(self.update_preview)
        self.title_input.textChanged.connect(self.update_preview)

        editor_layout = QVBoxLayout()
        editor_layout.addWidget(self.title_input)
        editor_layout.addWidget(self.editor)

        layout = QHBoxLayout()
        layout.addLayout(editor_layout)
        layout.addWidget(self.preview)

        self.setLayout(layout)
        self.setMinimumSize(800, 600)
        self.update_preview()

    def update_preview(self):
        full_md = f"# {self.title_input.text()}\n\n{self.editor.toPlainText()}"
        html = convert_markdown_to_html(full_md)
        self.preview.setHtml(html)

    def closeEvent(self, event: QCloseEvent):
        new_title = self.title_input.text()
        new_preview = self.editor.toPlainText()
        self.db.update_note(self.note_id, new_title, new_preview)
        super().closeEvent(event)
        if self.on_close:
            self.on_close()
