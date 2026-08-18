#!/usr/bin/env python3
"""Install the two Xiaohongshu custom agents into the active Codex home."""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import shutil
import sys
from datetime import datetime
import re

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10 and earlier
    tomllib = None


AGENT_FILES = (
    "xiaohongshu-product-image-reviewer.toml",
    "xiaohongshu-fact-copywriter.toml",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate(path: Path) -> None:
    required = ("name", "description", "developer_instructions")
    if tomllib is not None:
        with path.open("rb") as handle:
            data = tomllib.load(handle)
        missing = [key for key in required if not isinstance(data.get(key), str) or not data[key].strip()]
    else:
        text = path.read_text(encoding="utf-8")
        scalar_keys = re.findall(r'(?m)^(name|description)\s*=\s*"[^"\n]+"\s*$', text)
        instruction_match = re.search(
            r'(?ms)^developer_instructions\s*=\s*"""\s*\n.+?\n"""\s*$',
            text,
        )
        present = set(scalar_keys)
        if instruction_match:
            present.add("developer_instructions")
        missing = [key for key in required if key not in present]
    if missing:
        raise ValueError(f"{path.name} 缺少有效字段: {', '.join(missing)}")


def codex_home() -> Path:
    configured = os.environ.get("CODEX_HOME")
    return Path(configured).expanduser() if configured else Path.home() / ".codex"


def main() -> int:
    parser = argparse.ArgumentParser(description="安装或检查女装小红书 Codex 自定义 Agent")
    parser.add_argument("--check", action="store_true", help="只检查目标文件，不写入")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    source_dir = repo_root / "agents"
    destination_dir = codex_home() / "agents"
    failures: list[str] = []

    if not args.check:
        destination_dir.mkdir(parents=True, exist_ok=True)

    for filename in AGENT_FILES:
        source = source_dir / filename
        destination = destination_dir / filename
        try:
            validate(source)
            if args.check:
                if not destination.is_file():
                    raise FileNotFoundError(f"未安装: {destination}")
                validate(destination)
                if sha256(source) != sha256(destination):
                    raise ValueError(f"内容与仓库版本不一致: {destination}")
                print(f"ok\t{destination}")
                continue

            if destination.is_file() and sha256(source) == sha256(destination):
                print(f"skip\t{destination}\t内容已一致")
                continue

            if destination.exists() and not destination.is_file():
                raise ValueError(f"目标不是普通文件: {destination}")

            if destination.is_file():
                stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                backup = destination.with_name(f"{destination.name}.backup-{stamp}")
                shutil.copy2(destination, backup)
                print(f"backup\t{backup}")

            temporary = destination.with_suffix(destination.suffix + ".tmp")
            shutil.copy2(source, temporary)
            validate(temporary)
            temporary.replace(destination)
            print(f"installed\t{destination}")
        except (OSError, ValueError) as exc:
            failures.append(f"{filename}: {exc}")

    if failures:
        for failure in failures:
            print(f"error\t{failure}", file=sys.stderr)
        return 1

    if args.check:
        print("验证完成：两个 Agent 均已安装且内容一致。")
    else:
        print("安装完成。请再运行 scripts/install_agents.py --check，并新开 Codex 对话刷新 Agent 列表。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
