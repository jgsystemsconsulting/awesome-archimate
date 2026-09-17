# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: CC0-1.0
"""Release gate (RR-B-15) for Awesome ArchiMate (Base + list files)."""
import pathlib
import re
import subprocess
import sys

fails: list[str] = []

REQUIRED = [
    "LICENSE", "COPYRIGHT", "NOTICE", "README.md", "CHANGELOG.md",
    "RELEASE-INFO.txt", "CITATION.cff", "SECURITY.md", ".gitignore",
    "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "docs/DISTRIBUTION.md",
    "docs/index.html", "scripts/check_release.py",
]
for f in REQUIRED:
    if not pathlib.Path(f).is_file():
        fails.append(f"required file missing: {f}")

tracked = subprocess.run(
    ["git", "ls-files"], capture_output=True, text=True, check=True
).stdout.splitlines()
FORBIDDEN_PATH_PARTS = [
    "__pycache__", ".venv", ".worktrees", ".pytest_cache", ".ruff_cache", ".bak",
]
for f in tracked:
    if any(part in f for part in FORBIDDEN_PATH_PARTS):
        fails.append(f"forbidden tracked path: {f}")

FORBIDDEN_CONTENT = [
    re.compile(r"BEGIN [A-Z ]*PRIVATE KEY"),
]
SCAN_GLOBS = ["scripts/*.py", "*.md", "*.txt", "*.cff", "docs/**/*.md", "docs/**/*.html"]
scanned = 0
for g in SCAN_GLOBS:
    for path in pathlib.Path(".").glob(g):
        if not path.is_file():
            continue
        scanned += 1
        text = path.read_text(encoding="utf-8", errors="ignore")
        for rx in FORBIDDEN_CONTENT:
            if rx.search(text):
                fails.append(f"forbidden content in {path}: {rx.pattern}")

HEADER_SENTINEL = "Copyright (c) 2026 JG Systems Consulting Ltd"
for path in pathlib.Path("scripts").glob("*.py"):
    head = path.read_text(encoding="utf-8", errors="ignore")[:400]
    if HEADER_SENTINEL not in head:
        fails.append(f"header missing: {path}")
    if "SPDX-License-Identifier: CC0-1.0" not in head:
        fails.append(f"SPDX missing: {path}")

if scanned < 1:
    fails.append("SCAN_GLOBS matched zero files")

if fails:
    print("RELEASE GATE FAILED:")
    for f in fails:
        print(f"  - {f}")
    sys.exit(1)
print(f"release gate: PASS (scanned {scanned} files)")
