from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QMouseEvent, QPainter, QBrush

class NoteCard(QWidget):
    def __init__(self, note_id, title, date, preview, on_click):
        super().__init__()
        self.note_id = note_id
        self.title = title
        self.date = date
        self.preview = preview
        self.on_click = on_click

        self.setFixedSize(222, 120)
        self.setStyleSheet("padding: 10px; border-radius: 2px;")

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Отступы внутри карточки
        self.setLayout(layout)

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-weight: 400; font-size: 12px; color: white; background-color: #64032E;")
        self.title_label.setWordWrap(True)

        self.date_label = QLabel(date)
        self.date_label.setStyleSheet("font-size: 10px; color: #000;")
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.preview_label = QLabel(preview)
        self.preview_label.setStyleSheet("font-size: 10px; color: #000;")

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(12)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(0, 0, 0, 30))  # Прозрачность
        self.setGraphicsEffect(shadow)
        self.preview_label.setWordWrap(True)

        layout.addWidget(self.title_label)
        layout.addWidget(self.date_label)
        layout.addWidget(self.preview_label)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        radius = 4
        color = QColor("white")  # Цвет фона карточки

        painter.setBrush(QBrush(color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

        super().paintEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if self.on_click:
            self.on_click(self.note_id, self.title, self.preview)
