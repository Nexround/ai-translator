import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont

from translator_app.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("翻译助手")

    font = QFont()
    font.setFamily("Microsoft YaHei")
    font.setPointSize(10)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
