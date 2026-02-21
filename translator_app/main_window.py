from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QTextEdit, QPushButton, QStatusBar, QApplication,
    QMessageBox, QSplitter,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QShortcut, QKeySequence

from .config import Config
from .api_client import TranslateWorker
from .settings import SettingsDialog

TARGET_LANGUAGES = [
    "中文", "英文", "日文", "韩文",
    "法文", "德文", "西班牙文", "俄文", "葡萄牙文",
    "意大利文", "阿拉伯文", "泰文", "越南文",
]

STYLESHEET = """
QMainWindow {
    background: #f5f6fa;
}
QTextEdit {
    background: #ffffff;
    border: 1px solid #dcdfe6;
    border-radius: 6px;
    padding: 10px;
    font-size: 11pt;
    selection-background-color: #409eff;
}
QTextEdit:focus {
    border-color: #409eff;
}
QComboBox {
    background: #ffffff;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    padding: 4px 8px;
    min-width: 120px;
    font-size: 10pt;
}
QComboBox:hover {
    border-color: #409eff;
}
QComboBox::drop-down {
    border: none;
    width: 24px;
}
QPushButton {
    background: #409eff;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 7px 18px;
    font-size: 10pt;
}
QPushButton:hover {
    background: #66b1ff;
}
QPushButton:pressed {
    background: #3a8ee6;
}
QPushButton:disabled {
    background: #a0cfff;
}
QPushButton[secondary="true"] {
    background: #f0f2f5;
    color: #606266;
    border: 1px solid #dcdfe6;
}
QPushButton[secondary="true"]:hover {
    background: #e6e8eb;
}
QLabel {
    font-size: 10pt;
    color: #303133;
}
QStatusBar {
    font-size: 9pt;
    color: #909399;
}
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._config = Config()
        self._worker: TranslateWorker | None = None
        self.setWindowTitle("翻译助手")
        self.resize(920, 600)
        self.setStyleSheet(STYLESHEET)
        self._init_ui()
        self._restore_lang_selection()

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(16, 12, 16, 8)
        root.setSpacing(10)

        # Top bar: language selectors + settings button
        top_bar = QHBoxLayout()
        top_bar.setSpacing(8)

        top_bar.addWidget(QLabel("目标语言:"))
        self._combo_target = QComboBox()
        self._combo_target.addItems(TARGET_LANGUAGES)
        top_bar.addWidget(self._combo_target)

        top_bar.addStretch()

        self._btn_settings = QPushButton("⚙ 设置")
        self._btn_settings.setProperty("secondary", True)
        self._btn_settings.clicked.connect(self._on_open_settings)
        top_bar.addWidget(self._btn_settings)

        root.addLayout(top_bar)

        # Splitter with source / target text areas
        splitter = QSplitter(Qt.Orientation.Horizontal)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(6)
        self._edit_source = QTextEdit()
        self._edit_source.setPlaceholderText("在此输入要翻译的文本...")
        left_layout.addWidget(self._edit_source)
        left_btn_row = QHBoxLayout()
        left_btn_row.addStretch()
        self._btn_clear = QPushButton("清空")
        self._btn_clear.setProperty("secondary", True)
        self._btn_clear.setFixedWidth(70)
        self._btn_clear.clicked.connect(self._on_clear)
        left_btn_row.addWidget(self._btn_clear)
        left_layout.addLayout(left_btn_row)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(6)
        self._edit_target = QTextEdit()
        self._edit_target.setPlaceholderText("翻译结果将在这里显示...")
        self._edit_target.setReadOnly(True)
        right_layout.addWidget(self._edit_target)
        right_btn_row = QHBoxLayout()
        right_btn_row.addStretch()
        self._btn_copy = QPushButton("复制")
        self._btn_copy.setProperty("secondary", True)
        self._btn_copy.setFixedWidth(70)
        self._btn_copy.clicked.connect(self._on_copy)
        right_btn_row.addWidget(self._btn_copy)
        right_layout.addLayout(right_btn_row)

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        root.addWidget(splitter, 1)

        # Translate button
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self._btn_translate = QPushButton("翻译  (Ctrl+Enter)")
        self._btn_translate.setFixedHeight(38)
        self._btn_translate.setFixedWidth(180)
        self._btn_translate.clicked.connect(self._on_translate)
        btn_row.addWidget(self._btn_translate)
        btn_row.addStretch()
        root.addLayout(btn_row)

        # Status bar
        self._status_bar = QStatusBar()
        self.setStatusBar(self._status_bar)
        self._status_bar.showMessage("就绪")

        # Shortcut
        shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        shortcut.activated.connect(self._on_translate)

    def _restore_lang_selection(self):
        tgt = self._config.target_lang
        idx_tgt = self._combo_target.findText(tgt)
        if idx_tgt >= 0:
            self._combo_target.setCurrentIndex(idx_tgt)

    def _on_open_settings(self):
        dlg = SettingsDialog(self._config, self)
        dlg.exec()

    def _on_clear(self):
        self._edit_source.clear()
        self._edit_target.clear()
        self._status_bar.showMessage("已清空")

    def _on_copy(self):
        text = self._edit_target.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            self._status_bar.showMessage("已复制到剪贴板", 3000)

    def _on_translate(self):
        text = self._edit_source.toPlainText().strip()
        if not text:
            self._status_bar.showMessage("请输入要翻译的文本")
            return

        if not self._config.api_key:
            QMessageBox.warning(self, "提示", "请先在设置中配置 API Key。")
            return

        target_lang = self._combo_target.currentText()

        self._config.target_lang = target_lang
        self._config.save()

        self._cleanup_worker()

        self._edit_target.clear()
        self._btn_translate.setEnabled(False)
        self._btn_translate.setText("翻译中...")
        self._status_bar.showMessage("正在翻译...")

        self._worker = TranslateWorker(
            self._config, text, target_lang
        )
        self._worker.chunk_received.connect(self._on_chunk)
        self._worker.error_occurred.connect(self._on_error)
        self._worker.finished_signal.connect(self._on_finished)
        self._worker.start()

    def _cleanup_worker(self):
        if self._worker is not None:
            self._worker.chunk_received.disconnect()
            self._worker.error_occurred.disconnect()
            self._worker.finished_signal.disconnect()
            if self._worker.isRunning():
                self._worker.cancel()
                self._worker.wait(3000)
            self._worker = None

    def _on_chunk(self, text: str):
        self._edit_target.moveCursor(self._edit_target.textCursor().MoveOperation.End)
        self._edit_target.insertPlainText(text)

    def _on_error(self, msg: str):
        self._status_bar.showMessage(f"错误: {msg}")
        QMessageBox.critical(self, "翻译失败", msg)

    def _on_finished(self):
        self._btn_translate.setEnabled(True)
        self._btn_translate.setText("翻译  (Ctrl+Enter)")
        self._status_bar.showMessage("翻译完成", 5000)

    def closeEvent(self, event):
        self._cleanup_worker()
        super().closeEvent(event)
