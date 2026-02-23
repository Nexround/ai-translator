"""Nuitka build script. Usage: uv run python build.py [--dmg]"""

import argparse
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


APP_NAME = "TranslatorApp"
DIST_DIR = Path("dist")


def build_executable() -> Path:
    system = platform.system()

    cmd = [
        sys.executable,
        "-m",
        "nuitka",
        "--output-dir=dist",
        "--enable-plugin=pyside6",
        "--assume-yes-for-downloads",
        "main.py",
    ]

    if system == "Windows":
        cmd.extend(
            [
                "--mode=onefile",
                "--windows-console-mode=disable",
                f"--output-filename={APP_NAME}.exe",
            ]
        )
    elif system == "Darwin":
        cmd.extend(
            [
                "--mode=app",
                f"--output-filename={APP_NAME}",
            ]
        )
    else:
        cmd.extend(
            [
                "--mode=onefile",
                f"--output-filename={APP_NAME}",
            ]
        )

    subprocess.check_call(cmd)

    if system == "Windows":
        return DIST_DIR / f"{APP_NAME}.exe"
    if system == "Darwin":
        expected_app_path = DIST_DIR / f"{APP_NAME}.app"
        generated_apps = sorted(DIST_DIR.glob("*.app"))
        if not generated_apps:
            if expected_app_path.exists():
                return expected_app_path
            raise FileNotFoundError("No .app bundle generated in dist directory")

        generated_app_path = generated_apps[0]
        if expected_app_path.exists() and generated_app_path != expected_app_path:
            shutil.rmtree(expected_app_path)
        if generated_app_path != expected_app_path:
            generated_app_path.rename(expected_app_path)
        return expected_app_path
    return DIST_DIR / APP_NAME


def build_dmg(app_path: Path) -> Path:
    if platform.system() != "Darwin":
        raise RuntimeError("DMG packaging is only supported on macOS")
    if not app_path.exists():
        raise FileNotFoundError(f"App bundle not found: {app_path}")

    dmg_path = DIST_DIR / f"{APP_NAME}-macOS.dmg"
    if dmg_path.exists():
        dmg_path.unlink()

    with tempfile.TemporaryDirectory(prefix="translator-dmg-") as temp_dir:
        stage_dir = Path(temp_dir) / APP_NAME
        stage_dir.mkdir(parents=True, exist_ok=True)
        shutil.copytree(app_path, stage_dir / app_path.name)

        subprocess.check_call(
            [
                "hdiutil",
                "create",
                "-volname",
                APP_NAME,
                "-srcfolder",
                str(stage_dir),
                "-ov",
                "-format",
                "UDZO",
                str(dmg_path),
            ]
        )

    return dmg_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dmg", action="store_true", help="Build .dmg package on macOS"
    )
    args = parser.parse_args()

    artifact = build_executable()
    print(f"Built artifact: {artifact}")

    if args.dmg:
        dmg_path = build_dmg(artifact)
        print(f"Built DMG: {dmg_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
