from PyQt6.QtWidgets import QWidget, QLineEdit, QTextEdit, QTextBrowser, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QMessageBox
from PyQt6.QtGui import QCloseEvent
from app.markdown import convert_markdown_to_html

from db.db import NotesDB

class MarkdownEditor(QWidget):
    def __init__(self, note_id: int, title: str, preview: str, db: NotesDB, on_close=None):
        super().__init__()
        self.on_close = on_close
        self.note_id = note_id
        self.db = db

        # Основной стиль
        self.setStyleSheet("background-color: #F8F8F8; font-family: 'Segoe UI'; font-size: 14px; color: #000; border: 1px solid #64032E; border-radius: 4px;")

        # Поля ввода
        self.title_input = QLineEdit()
        self.title_input.setStyleSheet("padding: 10px; font-weight: bold; font-size: 16px; color: #64032E;")
        self.title_input.setText(title)

        self.editor = QTextEdit()
        self.editor.setStyleSheet("padding: 10px;")
        self.editor.setPlainText(preview)

        # Область предпросмотра
        self.preview = QTextBrowser()
        self.preview.setStyleSheet("padding: 10px; background-color: #64032E; color: white; border: 1px solid #64032E; border-radius: 4px;")

        # Подключения
        self.editor.textChanged.connect(self.update_preview)
        self.title_input.textChanged.connect(self.update_preview)

        # Схема компоновки
        editor_layout = QVBoxLayout()
        editor_layout.addWidget(self.title_input)
        editor_layout.addWidget(self.editor)

        content_layout = QHBoxLayout()
        content_layout.addLayout(editor_layout)
        content_layout.addWidget(self.preview)

        # Кнопки снизу
        self.save_button = QPushButton("Скачать в формате .md")
        self.save_button.setStyleSheet("background-color: #64032E; color: white; border-radius: 12px; padding: 10px;")

        self.close_button = QPushButton("Закрыть")
        self.close_button.setStyleSheet("background-color: #64032E; color: white; border-radius: 12px; padding: 10px;")

        self.delete_button = QPushButton("Удалить заметку")
        self.delete_button.setStyleSheet("background-color: #64032E; color: white; border-radius: 12px; padding: 10px;")

        self.save_button.clicked.connect(self.on_download_clicked)
        self.close_button.clicked.connect(self.on_close_clicked)
        self.delete_button.clicked.connect(self.on_delete_clicked)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.close_button)
        button_layout.addWidget(self.delete_button)

        # Основной вертикальный layout
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(content_layout)
        main_layout.addLayout(button_layout)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        self.setLayout(main_layout)
        self.setMinimumSize(800, 600)
        self.update_preview()

    def update_preview(self):
        full_md = f"# {self.title_input.text()}\n\n{self.editor.toPlainText()}"
        html = convert_markdown_to_html(full_md)
        self.preview.setHtml(html)

    from PyQt6.QtWidgets import QFileDialog

    def on_download_clicked(self):
        # Получаем заголовок и содержимое
        title = self.title_input.text()
        content = self.editor.toPlainText()
        full_md = f"# {title}\n\n{content}"

        # Диалог выбора файла
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить заметку",
            f"{title}.md",
            "Markdown Files (*.md)"
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(full_md)
            except Exception as e:
                print(f"Ошибка при сохранении файла: {e}")


    def on_save_clicked(self):
        new_title = self.title_input.text()
        new_preview = self.editor.toPlainText()
        self.db.update_note(self.note_id, new_title, new_preview)

    def on_close_clicked(self):
        self.close()


    def on_delete_clicked(self):
        confirm = QMessageBox.question(
            self,
            "Подтвердите удаление",
            "Вы уверены, что хотите удалить эту заметку?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            self.db.delete_note_by_id(self.note_id)
            self.close()
            if self.on_close:
                self.on_close()


    def closeEvent(self, event: QCloseEvent):
        # Перед закрытием сохраняем
        self.on_save_clicked()
        super().closeEvent(event)
        if self.on_close:
            self.on_close()
