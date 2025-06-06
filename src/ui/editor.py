# src/ui/editor.py
from PyQt6.QtWidgets import QWidget, QTextEdit, QTextBrowser, QHBoxLayout
from app.markdown import convert_markdown_to_html

class MarkdownEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.editor = QTextEdit()
        self.preview = QTextBrowser()

        self.editor.textChanged.connect(self.update_preview)

        layout = QHBoxLayout()
        layout.addWidget(self.editor)
        layout.addWidget(self.preview)
        self.setLayout(layout)

        self.setMinimumSize(800, 600)
        self.update_preview()

    def update_preview(self):
        md_text = self.editor.toPlainText()
        html = convert_markdown_to_html(md_text)
        self.preview.setHtml(html)
