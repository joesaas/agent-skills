#!/usr/bin/env python3
"""Structural checks for the agent-skills collection (no network)."""
import json
import py_compile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []

catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
for skill in catalog["skills"]:
    base = ROOT / "skills" / skill["name"]
    if not (base / "README.md").exists():
        errors.append(f"{skill['name']}: missing README.md")
    for runtime, variant in skill["variants"].items():
        pkg = ROOT / variant["path"]
        if not pkg.is_dir():
            errors.append(f"{skill['name']}/{runtime}: missing package dir {variant['path']}")
            continue
        if runtime == "generic":
            for required in ("AGENT_INSTRUCTIONS.md", "tool.json", "INSTALL.md"):
                if not (pkg / required).exists():
                    errors.append(f"{pkg}: missing {required}")
        else:
            if not (pkg / "SKILL.md").exists():
                errors.append(f"{pkg}: missing SKILL.md")
            if not (pkg / "INSTALL.md").exists():
                errors.append(f"{pkg}: missing INSTALL.md")
        if runtime == "muse" and not variant["package"].endswith("-muse"):
            errors.append("Muse package name must end with -muse")
        if runtime == "codex" and not (pkg / "agents/openai.yaml").exists():
            errors.append("codex package missing agents/openai.yaml")

for script in ROOT.rglob("upload_doc.py"):
    try:
        py_compile.compile(str(script), doraise=True)
    except py_compile.PyCompileError as exc:
        errors.append(f"{script}: {exc}")

for path in ROOT.rglob("*"):
    if path.is_file() and path.suffix in {".md", ".py", ".json", ".yaml"}:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "hsurr:" in text and "surrogate" not in text and "替身" not in text:
            errors.append(f"{path}: possible live surrogate value")

if errors:
    print("FAILED")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("OK: catalog, variants, Muse suffix, and Python syntax all valid")
