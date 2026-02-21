import traceback

from openai import OpenAI, APIConnectionError, APITimeoutError, APIStatusError
from PySide6.QtCore import QThread, Signal

from .config import Config, DEFAULT_SYSTEM_PROMPT


class TranslateWorker(QThread):
    chunk_received = Signal(str)
    finished_signal = Signal()
    error_occurred = Signal(str)

    def __init__(
        self,
        config: Config,
        text: str,
        target_lang: str,
    ):
        super().__init__()
        self._config = config
        self._text = text
        self._target_lang = target_lang
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    def _build_system_prompt(self) -> str:
        prompt_template = self._config.system_prompt or DEFAULT_SYSTEM_PROMPT
        return prompt_template.format(
            target_lang=self._target_lang,
        )

    def run(self):
        client = OpenAI(
            api_key=self._config.api_key,
            base_url=self._config.base_url,
            timeout=60.0,
        )

        try:
            system_prompt = self._build_system_prompt()

            stream = client.chat.completions.create(
                model=self._config.model,
                stream=True,
                messages=[
                    {"role": "user", "content": f"{system_prompt}\n\n{self._text}"},
                ],
            )

            accumulated = ""
            for chunk in stream:
                if self._cancelled:
                    stream.close()
                    return

                if not chunk.choices:
                    continue

                choice = chunk.choices[0]
                if choice.finish_reason is not None:
                    break

                delta_content = choice.delta.content if choice.delta else None
                if delta_content:
                    if len(delta_content) > len(accumulated) and delta_content.startswith(accumulated):
                        new_text = delta_content[len(accumulated):]
                    elif accumulated.endswith(delta_content):
                        continue
                    else:
                        new_text = delta_content
                    accumulated += new_text
                    self.chunk_received.emit(new_text)

        except APITimeoutError:
            self.error_occurred.emit("请求超时，请稍后重试。")
            raise
        except APIConnectionError:
            self.error_occurred.emit("无法连接到 API 服务器，请检查网络或 Base URL 设置。")
            raise
        except APIStatusError as e:
            self.error_occurred.emit(f"API 返回错误 ({e.status_code}): {e.message}")
            raise
        except Exception as e:
            self.error_occurred.emit(f"请求异常: {e}")
            traceback.print_exc()
            raise
        finally:
            if not self._cancelled:
                self.finished_signal.emit()


class TestConnectionWorker(QThread):
    success = Signal(str)
    error_occurred = Signal(str)

    def __init__(self, api_key: str, base_url: str, model: str):
        super().__init__()
        self._api_key = api_key
        self._base_url = base_url
        self._model = model

    def run(self):
        client = OpenAI(
            api_key=self._api_key,
            base_url=self._base_url,
            timeout=15.0,
        )

        try:
            client.chat.completions.create(
                model=self._model,
                max_tokens=5,
                messages=[{"role": "user", "content": "Hi"}],
            )
            self.success.emit("连接成功！API 配置有效。")
        except APITimeoutError:
            self.error_occurred.emit("连接超时。")
            raise
        except APIConnectionError:
            self.error_occurred.emit("无法连接到服务器，请检查 Base URL。")
            raise
        except APIStatusError as e:
            self.error_occurred.emit(f"API 返回错误 ({e.status_code}): {e.message}")
            raise
        except Exception as e:
            self.error_occurred.emit(f"连接失败: {e}")
            traceback.print_exc()
            raise
