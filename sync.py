#!/usr/bin/env python3
"""把本仓库（learning-workflow）的共享文件同步到一个学习仓库，并写入版本锁。

用法：
    python sync.py <学习仓库路径>

两个学习仓库用同一套三栏结构：阅读（自己读长文）、编程（GPT 带写）、动手（Muse）。
同步后，学习仓库的 `python start/scripts/progress.py --check` 会核对 start/WORKFLOW.lock：
共享文件被直接修改时 CI 会变红。要改共享文件，只改本仓库，再重新同步。
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
PROMPTS = ["coding-tutor.md", "coding-archiver.md", "hands-on.md"]
STALE = ["start/prompts/tutor.md", "start/prompts/archiver.md", "start/prompts/examiner.md", "start/prompts/setup.md",
         "start/prompts/theory-tutor.md", "start/prompts/theory-archiver.md", "start/prompts/theory-examiner.md",
         "start/prompts/practice-tutor.md", "start/prompts/practice-archiver.md",
         "start/templates/campaign-dual.md", "GEMINI.md"]


def plan() -> dict[str, Path]:
    """目标路径 → 源文件。"""
    files = {
        "AGENTS.md": KIT / "AGENTS.md",
        "start/RULES.md": KIT / "RULES.md",
        "start/scripts/progress.py": KIT / "scripts" / "progress.py",
    }
    for name in PROMPTS:
        files[f"start/prompts/{name}"] = KIT / "prompts" / name
    for t in sorted((KIT / "templates").glob("*.md")):
        files[f"start/templates/{t.name}"] = t
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("repo", type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    if not (repo / "start").is_dir():
        sys.exit(f"{repo} 不是学习仓库（缺少 start/）")

    files = plan()
    for rel in STALE:  # 旧结构留下的文件
        if (repo / rel).exists():
            (repo / rel).unlink()
            print(f"删除 {rel}")
    for rel, src in files.items():
        dst = repo / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)

    try:
        version = subprocess.run(["git", "-C", str(KIT), "rev-parse", "--short", "HEAD"],
                                 capture_output=True, text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        version = "未提交"
    lines = [f"# learning-workflow {version}：由 sync.py 生成，不要手动修改"]
    lines += [f"{hashlib.sha256((repo / rel).read_bytes()).hexdigest()}  {rel}" for rel in sorted(files)]
    (repo / "start" / "WORKFLOW.lock").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"已同步 {len(files)} 个共享文件到 {repo}（learning-workflow {version}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
