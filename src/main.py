import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

def load_stylesheet(path: str) -> str:
    with open(path, "r") as f:
        return f.read()

def main():
    app = QApplication(sys.argv)

    # Запускаем главное окно
    window = MainWindow()

    stylesheet = load_stylesheet("resources/style.qss")
    app.setStyleSheet(stylesheet)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
