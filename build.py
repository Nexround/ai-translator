"""Nuitka build script. Usage: uv run build"""

import subprocess
import sys


def main():
    cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",
        "--onefile",
        "--windows-console-mode=disable",
        "--output-dir=dist",
        "--output-filename=TranslatorApp.exe",
        "--enable-plugin=pyside6",
        "--assume-yes-for-downloads",
        "main.py",
    ]
    raise SystemExit(subprocess.call(cmd))


if __name__ == "__main__":
    main()
