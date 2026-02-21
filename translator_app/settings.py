from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QPushButton, QTabWidget, QWidget, QMessageBox,
    QFormLayout,
)

from .config import Config, DEFAULT_SYSTEM_PROMPT
from .api_client import TestConnectionWorker


class SettingsDialog(QDialog):
    def __init__(self, config: Config, parent=None):
        super().__init__(parent)
        self._config = config
        self._test_worker: TestConnectionWorker | None = None
        self.setWindowTitle("设置")
        self.setMinimumSize(520, 420)
        self._init_ui()
        self._load_values()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        self._tabs = QTabWidget()
        self._tabs.addTab(self._create_api_tab(), "API 设置")
        self._tabs.addTab(self._create_prompt_tab(), "提示词设置")
        layout.addWidget(self._tabs)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self._btn_save = QPushButton("保存")
        self._btn_save.setFixedWidth(90)
        self._btn_save.clicked.connect(self._on_save)
        self._btn_cancel = QPushButton("取消")
        self._btn_cancel.setFixedWidth(90)
        self._btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(self._btn_save)
        btn_layout.addWidget(self._btn_cancel)
        layout.addLayout(btn_layout)

    def _create_api_tab(self) -> QWidget:
        tab = QWidget()
        form = QFormLayout(tab)
        form.setContentsMargins(12, 16, 12, 12)
        form.setSpacing(12)

        self._edit_api_key = QLineEdit()
        self._edit_api_key.setEchoMode(QLineEdit.EchoMode.Password)
        self._edit_api_key.setPlaceholderText("sk-...")
        form.addRow("API Key:", self._edit_api_key)

        self._edit_base_url = QLineEdit()
        self._edit_base_url.setPlaceholderText("https://api.openai.com/v1")
        form.addRow("Base URL:", self._edit_base_url)

        self._edit_model = QLineEdit()
        self._edit_model.setPlaceholderText("gpt-4o-mini")
        form.addRow("模型:", self._edit_model)

        self._btn_test = QPushButton("测试连接")
        self._btn_test.setFixedWidth(120)
        self._btn_test.clicked.connect(self._on_test_connection)
        form.addRow("", self._btn_test)

        return tab

    def _create_prompt_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(12, 16, 12, 12)
        layout.setSpacing(10)

        help_label = QLabel(
            "自定义发送给大模型的系统提示词。\n"
            "{target_lang} = 目标语言"
        )
        help_label.setWordWrap(True)
        help_label.setStyleSheet("color: #666; font-size: 9pt;")
        layout.addWidget(help_label)

        self._edit_prompt = QTextEdit()
        self._edit_prompt.setPlaceholderText("输入系统提示词...")
        layout.addWidget(self._edit_prompt)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self._btn_restore = QPushButton("恢复默认")
        self._btn_restore.setFixedWidth(100)
        self._btn_restore.clicked.connect(self._on_restore_default)
        btn_row.addWidget(self._btn_restore)
        layout.addLayout(btn_row)

        return tab

    def _load_values(self):
        self._edit_api_key.setText(self._config.api_key)
        self._edit_base_url.setText(self._config.base_url)
        self._edit_model.setText(self._config.model)
        self._edit_prompt.setPlainText(self._config.system_prompt)

    def _on_save(self):
        self._config.api_key = self._edit_api_key.text().strip()
        self._config.base_url = self._edit_base_url.text().strip() or "https://api.openai.com/v1"
        self._config.model = self._edit_model.text().strip() or "gpt-4o-mini"
        self._config.system_prompt = self._edit_prompt.toPlainText().strip() or DEFAULT_SYSTEM_PROMPT
        self._config.save()
        self.accept()

    def _on_restore_default(self):
        self._edit_prompt.setPlainText(DEFAULT_SYSTEM_PROMPT)

    def _on_test_connection(self):
        api_key = self._edit_api_key.text().strip()
        base_url = self._edit_base_url.text().strip() or "https://api.openai.com/v1"
        model = self._edit_model.text().strip() or "gpt-4o-mini"

        if not api_key:
            QMessageBox.warning(self, "提示", "请先输入 API Key。")
            return

        self._btn_test.setEnabled(False)
        self._btn_test.setText("测试中...")

        self._test_worker = TestConnectionWorker(api_key, base_url, model)
        self._test_worker.success.connect(self._on_test_success)
        self._test_worker.error_occurred.connect(self._on_test_error)
        self._test_worker.finished.connect(self._on_test_done)
        self._test_worker.start()

    def _on_test_success(self, msg: str):
        QMessageBox.information(self, "测试结果", msg)

    def _on_test_error(self, msg: str):
        QMessageBox.critical(self, "测试失败", msg)

    def _on_test_done(self):
        self._btn_test.setEnabled(True)
        self._btn_test.setText("测试连接")
