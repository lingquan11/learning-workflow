#!/usr/bin/env python3
"""把本仓库（learning-workflow）的共享文件同步到一个学习仓库，并写入版本锁。

用法：
    python sync.py <学习仓库路径>           # 单线仓库（导师 + Gemini 考官 + Muse 环境）
    python sync.py <学习仓库路径> --dual    # 双线仓库（理论 GPT / 实践 Muse / Gemini 考官）

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
COMMON_PROMPTS = ["examiner.md", "setup.md"]
SINGLE_PROMPTS = ["tutor.md", "archiver.md"]
DUAL_PROMPTS = ["theory-tutor.md", "theory-archiver.md", "practice-tutor.md", "practice-archiver.md"]


def plan(dual: bool) -> dict[str, Path]:
    """目标路径 → 源文件。"""
    files = {
        "AGENTS.md": KIT / ("AGENTS-dual.md" if dual else "AGENTS.md"),
        "GEMINI.md": KIT / "GEMINI.md",
        "start/RULES.md": KIT / "RULES.md",
        "start/scripts/progress.py": KIT / "scripts" / "progress.py",
    }
    for name in COMMON_PROMPTS + SINGLE_PROMPTS * (not dual):
        files[f"start/prompts/{name}"] = KIT / "prompts" / name
    for name in DUAL_PROMPTS * dual:
        files[f"start/prompts/{name}"] = KIT / "prompts-dual" / name
    for t in sorted((KIT / "templates").glob("*.md")):
        files[f"start/templates/{t.name}"] = t
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("repo", type=Path)
    parser.add_argument("--dual", action="store_true", help="双线仓库")
    args = parser.parse_args()
    repo = args.repo.resolve()
    if not (repo / "start").is_dir():
        sys.exit(f"{repo} 不是学习仓库（缺少 start/）")

    files = plan(args.dual)
    # 删掉另一种模式的提示词，避免两套并存
    for name in (SINGLE_PROMPTS if args.dual else DUAL_PROMPTS) + ["theory-examiner.md"]:
        stale = repo / "start" / "prompts" / name
        if stale.exists():
            stale.unlink()
            print(f"删除 start/prompts/{name}")
    for rel, src in files.items():
        dst = repo / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)

    try:
        version = subprocess.run(["git", "-C", str(KIT), "rev-parse", "--short", "HEAD"],
                                 capture_output=True, text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        version = "未提交"
    lines = [f"# learning-workflow {version}（{'双线' if args.dual else '单线'}）：由 sync.py 生成，不要手动修改"]
    lines += [f"{hashlib.sha256((repo / rel).read_bytes()).hexdigest()}  {rel}" for rel in sorted(files)]
    (repo / "start" / "WORKFLOW.lock").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"已同步 {len(files)} 个共享文件到 {repo}（learning-workflow {version}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
