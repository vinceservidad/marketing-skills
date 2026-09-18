#!/usr/bin/env python3
"""Build self-contained Agent Skills bundles from canonical Marketing Skills sources.

Canonical source remains .agents/skills/. The generated skills/ tree exists only
for portable distribution through tools such as the Vercel `skills` CLI.

Run:
    python3 scripts/build-portable-skills.py
    python3 scripts/build-portable-skills.py --check
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / ".agents" / "skills"
OUTPUT = ROOT / "skills"
README = "README.md"
MANIFEST = "PORTABLE-MANIFEST.json"
SCHEMA_VERSION = 1

BASE_SHARED = (
    "AGENTS.md",
    "GLOSSARY.md",
    "KNOWLEDGE-TAXONOMY.md",
    "PLATFORM-CURRENCY.md",
    "CAPABILITY-REGISTRY.md",
)

FRONTMATTER = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)
LINK = re.compile(r"(?P<prefix>!?\[[^\]]*\]\()(?P<target>[^)]+)(?P<close>\))")
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")

GENERATED_NOTE = (
    "\n<!-- GENERATED PORTABLE SKILL. Canonical source: .agents/skills/. DO NOT EDIT HERE. -->\n"
    "Before using this skill, read the bundled "
    "[Marketing Skills operating rules](_shared/AGENTS.md). "
    "The bundled shared files are generated dependencies, not a second source of truth.\n"
)


class BuildError(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise BuildError(message)


def inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def reject_symlink(path: Path) -> None:
    current = path
    while True:
        if current.is_symlink():
            raise BuildError(f"Symlink source is not supported: {current.relative_to(ROOT)}")
        if current == ROOT:
            break
        if ROOT not in current.parents:
            break
        current = current.parent


def all_files(directory: Path) -> list[Path]:
    reject_symlink(directory)
    result = []
    for path in sorted(directory.rglob("*")):
        if path.is_symlink():
            raise BuildError(f"Symlink source is not supported: {path.relative_to(ROOT)}")
        if path.is_file():
            result.append(path.resolve())
    return result


def local_target(source: Path, raw_target: str) -> tuple[Path, str] | None:
    target = raw_target.strip()
    if not target or target.startswith("#"):
        return None

    # Markdown titles after a URL are intentionally unsupported in canonical
    # internal links; external links remain untouched.
    if target.startswith("<") and ">" in target:
        path_part, remainder = target[1:].split(">", 1)
        suffix = remainder
    else:
        parts = target.split(maxsplit=1)
        path_part = parts[0]
        suffix = (" " + parts[1]) if len(parts) == 2 else ""

    parsed = urlsplit(path_part)
    if parsed.scheme or parsed.netloc or path_part.startswith(("mailto:", "data:", "/")):
        return None
    if not parsed.path:
        return None

    resolved = (source.parent / unquote(parsed.path)).resolve()
    try:
        resolved.relative_to(ROOT)
    except ValueError as exc:
        raise BuildError(
            f"Local link escapes repository: {source.relative_to(ROOT)} -> {raw_target}"
        ) from exc

    if not resolved.exists():
        raise BuildError(
            f"Broken local link: {source.relative_to(ROOT)} -> {raw_target}"
        )
    fragment = ("#" + parsed.fragment) if parsed.fragment else ""
    return resolved, fragment + suffix


def destination_for(source: Path, skill_root: Path, skill_name: str) -> Path:
    if inside(source, skill_root):
        return Path(skill_name) / source.relative_to(skill_root)
    return Path(skill_name) / "_shared" / source.relative_to(ROOT)


def add_path(path: Path, included: set[Path], queue: list[Path]) -> None:
    reject_symlink(path)
    if path.is_dir():
        for file in all_files(path):
            if file not in included:
                included.add(file)
                queue.append(file)
    elif path.is_file():
        path = path.resolve()
        if path not in included:
            included.add(path)
            queue.append(path)
    else:
        raise BuildError(f"Unsupported dependency: {path.relative_to(ROOT)}")


def collect_sources(skill_root: Path) -> set[Path]:
    included: set[Path] = set()
    queue: list[Path] = []

    add_path(skill_root, included, queue)
    for relative in BASE_SHARED:
        add_path((ROOT / relative).resolve(), included, queue)

    scanned: set[Path] = set()
    while queue:
        source = queue.pop()
        if source in scanned:
            continue
        scanned.add(source)
        if source.suffix.lower() != ".md":
            continue

        text = source.read_text(encoding="utf-8")
        for match in LINK.finditer(text):
            resolved = local_target(source, match.group("target"))
            if resolved is None:
                continue
            target, _ = resolved
            add_path(target, included, queue)

    return included


def rewrite_markdown(
    source: Path,
    destination: Path,
    text: str,
    included: set[Path],
    skill_root: Path,
    skill_name: str,
) -> str:
    def replace(match: re.Match[str]) -> str:
        resolved = local_target(source, match.group("target"))
        if resolved is None:
            return match.group(0)

        target, suffix = resolved
        target_file = target
        if target.is_dir():
            # Keep directory links as directories while ensuring their contents
            # were included by dependency collection.
            mapped = destination_for(target, skill_root, skill_name)
        else:
            require(target_file.resolve() in included, f"Unbundled dependency: {target_file}")
            mapped = destination_for(target_file.resolve(), skill_root, skill_name)

        relative = Path(os.path.relpath(mapped, destination.parent)).as_posix()
        original_path = match.group("target").split(maxsplit=1)[0]
        if original_path.rstrip("#").endswith("/") and not relative.endswith("/"):
            relative += "/"
        return f"{match.group('prefix')}{relative}{suffix}{match.group('close')}"

    return LINK.sub(replace, text)


def render_skill(skill_root: Path) -> dict[str, bytes]:
    skill_name = skill_root.name
    require(NAME.fullmatch(skill_name) is not None, f"Invalid skill folder name: {skill_name}")
    skill_md = skill_root / "SKILL.md"
    require(skill_md.is_file(), f"Missing SKILL.md: {skill_name}")

    included = collect_sources(skill_root)
    output: dict[str, bytes] = {}

    for source in sorted(included):
        destination = destination_for(source, skill_root, skill_name)
        if source.suffix.lower() == ".md":
            text = source.read_text(encoding="utf-8")
            text = rewrite_markdown(
                source, destination, text, included, skill_root, skill_name
            )
            if source == skill_md.resolve():
                match = FRONTMATTER.match(text)
                require(match is not None, f"Malformed frontmatter: {skill_name}/SKILL.md")
                text = text[: match.end()] + GENERATED_NOTE + text[match.end() :]
            output[destination.as_posix()] = text.encode("utf-8")
        else:
            output[destination.as_posix()] = source.read_bytes()

    return output


def render() -> dict[str, bytes]:
    require(CANONICAL.is_dir(), "Missing canonical .agents/skills directory")
    skills = sorted(path for path in CANONICAL.iterdir() if path.is_dir())
    require(bool(skills), "No canonical skills found")

    output: dict[str, bytes] = {}
    manifest_skills = {}

    for skill in skills:
        bundle = render_skill(skill.resolve())
        overlap = set(output) & set(bundle)
        require(not overlap, f"Portable output collision: {sorted(overlap)}")
        output.update(bundle)

        files = {
            str(Path(path).relative_to(skill.name)): hashlib.sha256(data).hexdigest()
            for path, data in sorted(bundle.items())
        }
        manifest_skills[skill.name] = {
            "source": f".agents/skills/{skill.name}",
            "file_count": len(files),
            "files": files,
        }

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "generated": True,
        "canonical_source": ".agents/skills",
        "skill_count": len(skills),
        "skills": manifest_skills,
    }
    output[MANIFEST] = (
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    return output


def actual_generated() -> dict[str, bytes]:
    if not OUTPUT.is_dir():
        return {}
    result = {}
    for path in sorted(OUTPUT.rglob("*")):
        if path.is_symlink():
            result[path.relative_to(OUTPUT).as_posix()] = b"__SYMLINK__"
        elif path.is_file():
            relative = path.relative_to(OUTPUT).as_posix()
            if relative == README:
                continue
            result[relative] = path.read_bytes()
    return result


def drift(expected: dict[str, bytes]) -> list[str]:
    actual = actual_generated()
    return sorted(
        path
        for path in actual.keys() | expected.keys()
        if actual.get(path) != expected.get(path)
    )


def previous_managed_names() -> set[str]:
    manifest = OUTPUT / MANIFEST
    if not manifest.is_file():
        return set()
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
        names = data.get("skills", {})
        if not isinstance(names, dict):
            raise ValueError
        return set(names)
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        raise BuildError(f"Invalid existing {MANIFEST}; review manually before rebuilding") from exc


def write(expected: dict[str, bytes]) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    require((OUTPUT / README).is_file(), f"{README} must remain a hand-maintained distribution guide")

    current_names = {
        path.name for path in CANONICAL.iterdir() if path.is_dir()
    }
    managed_names = previous_managed_names() | current_names

    for name in sorted(managed_names):
        target = OUTPUT / name
        if target.is_symlink():
            raise BuildError(f"Refusing generated skill symlink: {target}")
        if target.exists():
            require(target.is_dir(), f"Generated skill path is not a directory: {target}")
            shutil.rmtree(target)

    manifest = OUTPUT / MANIFEST
    if manifest.exists() or manifest.is_symlink():
        require(not manifest.is_symlink(), f"Refusing manifest symlink: {manifest}")
        manifest.unlink()

    # Refuse unrelated executable skill folders. The generated layer should be
    # deterministic and must not become a second hand-edited source hierarchy.
    for child in OUTPUT.iterdir():
        if child.name in {README, MANIFEST}:
            continue
        if child.is_dir() and (child / "SKILL.md").exists():
            raise BuildError(f"Unmanaged portable skill directory: {child}")

    for relative, data in expected.items():
        target = OUTPUT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)


def validate_links(expected: dict[str, bytes]) -> None:
    paths = {Path(path) for path in expected}
    for relative, data in expected.items():
        path = Path(relative)
        if path.suffix.lower() != ".md":
            continue
        text = data.decode("utf-8")
        for match in LINK.finditer(text):
            target = match.group("target").strip().split(maxsplit=1)[0]
            if not target or target.startswith(("#", "http:", "https:", "mailto:", "data:", "/")):
                continue
            parsed = urlsplit(target)
            candidate = (path.parent / unquote(parsed.path))
            normalized = Path(os.path.normpath(candidate.as_posix()))
            if parsed.path.endswith("/"):
                # A directory dependency is valid if at least one generated file
                # lives beneath it.
                if not any(p == normalized or normalized in p.parents for p in paths):
                    raise BuildError(f"Unresolved portable directory link: {relative} -> {target}")
            elif normalized not in paths:
                raise BuildError(f"Unresolved portable link: {relative} -> {target}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail when skills/ differs from canonical generated output")
    args = parser.parse_args(argv)

    try:
        expected = render()
        validate_links(expected)
        if args.check:
            changed = drift(expected)
            if changed:
                print("Portable skills differ from canonical sources:", file=sys.stderr)
                for path in changed:
                    print(f"- skills/{path}", file=sys.stderr)
                print("Run python3 scripts/build-portable-skills.py and review the result.", file=sys.stderr)
                return 1
            print(f"Portable skills are in sync ({len(json.loads(expected[MANIFEST])['skills'])} skills).")
            return 0

        write(expected)
        print(f"Built {len(json.loads(expected[MANIFEST])['skills'])} portable skills in {OUTPUT}.")
        return 0
    except (BuildError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"Portable skill build failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
