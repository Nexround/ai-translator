# Translator App

[中文文档](README.zh-CN.md)

A desktop translation tool powered by OpenAI-compatible APIs, featuring streaming output, multi-language support, and customizable prompts.

## Features

- **Multi-language** — Supports 13 target languages including Chinese, English, Japanese, Korean, French, German, and more
- **Streaming output** — Translation results appear in real time, token by token
- **Custom API** — Works with any OpenAI-compatible API (OpenAI, DeepSeek, Ollama, etc.)
- **Custom prompts** — Edit the system prompt to fine-tune translation style
- **Connection test** — One-click API configuration verification
- **Keyboard shortcut** — `Ctrl+Enter` to translate instantly

## Getting Started

### Download

Head to [Releases](../../releases/latest) and download the package for your OS:

- Windows: `TranslatorApp.exe`
- macOS: `TranslatorApp.app` (or `TranslatorApp-macOS.dmg`)

Double-click to run — no installation required.

On first launch, click the **Settings** button in the top-right corner to configure your API Key and Base URL.

### Run from Source

Requires Python 3.10+ and [uv](https://docs.astral.sh/uv/):

```bash
git clone https://github.com/<your-username>/translator.git
cd translator

uv sync
uv run python main.py
```

### Build Executable

```bash
uv sync --all-groups
uv run python build.py
```

- Windows output: `dist/TranslatorApp.exe`
- macOS output: `dist/TranslatorApp.app`

Build macOS DMG package:

```bash
uv run python build.py --dmg
```

DMG output: `dist/TranslatorApp-macOS.dmg`

## Configuration

| Option        | Description                                                                         | Default                     |
| ------------- | ----------------------------------------------------------------------------------- | --------------------------- |
| API Key       | LLM API key                                                                         | —                           |
| Base URL      | API endpoint                                                                        | `https://api.openai.com/v1` |
| Model         | Model name                                                                          | `gpt-4o-mini`               |
| System Prompt | Instruction sent to the model; `{target_lang}` is replaced with the target language | Built-in default            |

Configuration is stored in `~/.translator/config.json`.

## Tech Stack

- **GUI** — [PySide6](https://doc.qt.io/qtforpython-6/) (Qt for Python)
- **API** — [OpenAI Python SDK](https://github.com/openai/openai-python)
- **Packaging** — [Nuitka](https://nuitka.net/)
- **Dependency management** — [uv](https://docs.astral.sh/uv/)

## Release

Push a version tag to automatically build and publish a GitHub Release:

```bash
git tag v0.1.0
git push origin v0.1.0
```

GitHub Actions will build the executable on Windows and create a Release with the artifact attached.

## License

MIT
