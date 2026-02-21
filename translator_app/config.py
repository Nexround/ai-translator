import json
import traceback
from pathlib import Path

DEFAULT_SYSTEM_PROMPT = (
    "你是一个专业翻译助手。请将以下文本翻译为{target_lang}，"
    "自动识别源语言，只输出翻译结果，不要添加任何解释。"
)

DEFAULTS = {
    "api_key": "",
    "base_url": "https://api.openai.com/v1",
    "model": "gpt-4o-mini",
    "system_prompt": DEFAULT_SYSTEM_PROMPT,
    "target_lang": "英文",
}

CONFIG_DIR = Path.home() / ".translator"
CONFIG_FILE = CONFIG_DIR / "config.json"


class Config:
    def __init__(self):
        self._data: dict = dict(DEFAULTS)
        self.load()

    def load(self):
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                for key in DEFAULTS:
                    if key in saved:
                        self._data[key] = saved[key]
            except (json.JSONDecodeError, OSError):
                traceback.print_exc()

    def save(self):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    def get(self, key: str):
        return self._data.get(key, DEFAULTS.get(key))

    def set(self, key: str, value):
        self._data[key] = value

    @property
    def api_key(self) -> str:
        return self.get("api_key")

    @api_key.setter
    def api_key(self, value: str):
        self.set("api_key", value)

    @property
    def base_url(self) -> str:
        return self.get("base_url")

    @base_url.setter
    def base_url(self, value: str):
        self.set("base_url", value)

    @property
    def model(self) -> str:
        return self.get("model")

    @model.setter
    def model(self, value: str):
        self.set("model", value)

    @property
    def system_prompt(self) -> str:
        return self.get("system_prompt")

    @system_prompt.setter
    def system_prompt(self, value: str):
        self.set("system_prompt", value)

    @property
    def target_lang(self) -> str:
        return self.get("target_lang")

    @target_lang.setter
    def target_lang(self, value: str):
        self.set("target_lang", value)
