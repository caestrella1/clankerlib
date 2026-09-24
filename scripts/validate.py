#!/usr/bin/env python3
"""Validate library entries and keep manifest.json in sync with the files on disk.

Checks:
  - every skill/instruction/prompt has frontmatter with `name` and `description`
  - `name` is kebab-case, <= 64 chars, and matches its folder (skills) or file stem
  - `description` is <= 1024 chars (Agent Skills spec: https://agentskills.io/specification)
  - every manifest entry points to an existing path with matching name/description
  - every entry on disk is listed in the manifest (templates excluded)
  - copies bundled into skills match their source (see SYNCED_COPIES)

Usage: python3 scripts/validate.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
errors = []

# Skills must work when copied alone, so some bundle a copy of a shared file.
# copy path -> source path
SYNCED_COPIES = {
    "skills/declank/references/human-mode.md": "instructions/human-mode.md",
}


def parse_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    fields = {}
    for line in text[4:end].splitlines():
        # Top-level scalar keys only; nested YAML (e.g. prompt variables) is ignored.
        match = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
        if match:
            fields[match.group(1)] = match.group(2).strip().strip("\"'")
    return fields


def discover():
    """Return {section: {name: (entry_file, manifest_path)}} for entries on disk."""
    found = {"skills": {}, "instructions": {}, "prompts": {}}
    for skill_md in sorted((ROOT / "skills").glob("*/SKILL.md")):
        if skill_md.parent.name.startswith("_"):
            continue
        found["skills"][skill_md.parent.name] = (skill_md, skill_md.parent)
    for section in ("instructions", "prompts"):
        for md in sorted((ROOT / section).rglob("*.md")):
            if md.name.startswith("_"):
                continue
            found[section][md.stem] = (md, md)
    return found


def rel(path):
    return path.relative_to(ROOT).as_posix()


def main():
    found = discover()

    for section, entries in found.items():
        for expected_name, (entry_file, _) in entries.items():
            fm = parse_frontmatter(entry_file)
            if fm is None:
                errors.append(f"{rel(entry_file)}: missing or malformed frontmatter")
                continue
            for key in ("name", "description"):
                if not fm.get(key):
                    errors.append(f"{rel(entry_file)}: frontmatter missing `{key}`")
            name = fm.get("name", "")
            if name and (not NAME_RE.match(name) or len(name) > 64):
                errors.append(f"{rel(entry_file)}: name `{name}` must be kebab-case, max 64 chars")
            if len(fm.get("description", "")) > 1024:
                errors.append(f"{rel(entry_file)}: description exceeds 1024 chars")
            if name and name != expected_name:
                errors.append(f"{rel(entry_file)}: name `{name}` does not match `{expected_name}`")

    try:
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"manifest.json: {exc}")
        manifest = {}

    for section, entries in found.items():
        listed = {}
        for item in manifest.get(section, []):
            name = item.get("name", "")
            if name in listed:
                errors.append(f"manifest.json: duplicate {section} entry `{name}`")
            listed[name] = item
            if name not in entries:
                errors.append(f"manifest.json: {section} entry `{name}` not found on disk")
                continue
            entry_file, entry_path = entries[name]
            if item.get("path") != rel(entry_path):
                errors.append(f"manifest.json: `{name}` path should be `{rel(entry_path)}`")
            fm = parse_frontmatter(entry_file) or {}
            if item.get("description") != fm.get("description"):
                errors.append(f"manifest.json: `{name}` description differs from {rel(entry_file)}")
        for name in entries:
            if name not in listed:
                errors.append(f"manifest.json: {section} `{name}` exists on disk but is not listed")

    for copy, source in SYNCED_COPIES.items():
        copy_path, source_path = ROOT / copy, ROOT / source
        if not copy_path.is_file() or copy_path.read_bytes() != source_path.read_bytes():
            errors.append(f"{copy} is out of sync; run: cp {source} {copy}")

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"  - {err}")
        return 1
    total = sum(len(e) for e in found.values())
    print(f"OK: {total} entries validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
