# 翻译助手

[English](README.md)

一款基于 OpenAI 兼容 API 的桌面翻译工具，支持流式输出、多语言翻译和自定义提示词。

## 功能特性

- **多语言翻译** — 支持中文、英文、日文、韩文、法文、德文等 13 种目标语言
- **流式输出** — 翻译结果实时逐字显示，无需等待完整响应
- **自定义 API** — 兼容任何 OpenAI 格式的 API（OpenAI、DeepSeek、Ollama 等）
- **自定义提示词** — 可编辑系统提示词以调整翻译风格
- **连接测试** — 一键验证 API 配置是否正确
- **快捷键** — `Ctrl+Enter` 快速翻译

## 快速开始

### 下载使用

前往 [Releases](../../releases/latest) 页面下载对应系统的程序：

- Windows：`TranslatorApp.exe`
- macOS：`TranslatorApp.app`（或 `TranslatorApp-macOS.dmg`）

双击即可运行，无需安装。

首次使用请点击右上角「设置」按钮，配置 API Key 和 Base URL。

### 从源码运行

需要 Python 3.10+ 和 [uv](https://docs.astral.sh/uv/)：

```bash
git clone https://github.com/<your-username>/translator.git
cd translator

uv sync
uv run python main.py
```

### 本地打包

```bash
uv sync --all-groups
uv run python build.py
```

- Windows 产物：`dist/TranslatorApp.exe`
- macOS 产物：`dist/TranslatorApp.app`

生成 macOS DMG 安装包：

```bash
uv run python build.py --dmg
```

DMG 产物：`dist/TranslatorApp-macOS.dmg`

## 配置说明

| 配置项     | 说明                                               | 默认值                      |
| ---------- | -------------------------------------------------- | --------------------------- |
| API Key    | 大模型 API 密钥                                    | —                           |
| Base URL   | API 端点地址                                       | `https://api.openai.com/v1` |
| 模型       | 使用的模型名称                                     | `gpt-4o-mini`               |
| 系统提示词 | 发送给模型的指令，`{target_lang}` 会替换为目标语言 | 内置默认提示词              |

配置文件保存在 `~/.translator/config.json`。

## 技术栈

- **GUI** — [PySide6](https://doc.qt.io/qtforpython-6/) (Qt for Python)
- **API** — [OpenAI Python SDK](https://github.com/openai/openai-python)
- **打包** — [Nuitka](https://nuitka.net/)
- **依赖管理** — [uv](https://docs.astral.sh/uv/)

## 发布

推送版本标签即可自动构建并发布 Release：

```bash
git tag v0.1.0
git push origin v0.1.0
```

GitHub Actions 会自动完成打包并创建包含可执行文件的 Release。

## 许可证

MIT
