#!/usr/bin/env python3
"""Create code.zip without dataset, caches, virtual environments, or secrets."""
from pathlib import Path
import zipfile
ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "code.zip"
INCLUDE = [ROOT / "README.md", ROOT / "code"]
EXCLUDE_PARTS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache"}
EXCLUDE_SUFFIXES = {".pyc", ".pyo", ".zip", ".tar", ".gz", ".tgz", ".7z", ".rar"}
EXCLUDE_NAMES = {".env", ".env.local", ".DS_Store"}
with zipfile.ZipFile(DEST, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for base in INCLUDE:
        if base.is_file():
            archive.write(base, base.relative_to(ROOT))
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(ROOT)
            if any(part in EXCLUDE_PARTS for part in rel.parts):
                continue
            if path.name in EXCLUDE_NAMES or path.suffix.lower() in EXCLUDE_SUFFIXES:
                continue
            archive.write(path, rel)
print(f"Created {DEST} ({DEST.stat().st_size:,} bytes)")
