"""Regression checks for generated portable Agent Skills distribution."""

import importlib.util
import json
import os
from pathlib import Path
import unittest
from urllib.parse import unquote, urlsplit


REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "portable_skills", REPO / "scripts/build-portable-skills.py"
)
PORTABLE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PORTABLE)


class PortableSkillTests(unittest.TestCase):
    def test_render_covers_every_canonical_skill(self):
        output = PORTABLE.render()
        manifest = json.loads(output[PORTABLE.MANIFEST])
        canonical = sorted(
            path.name
            for path in (REPO / ".agents/skills").iterdir()
            if path.is_dir()
        )
        self.assertEqual(manifest["skill_count"], len(canonical))
        self.assertEqual(sorted(manifest["skills"]), canonical)
        for name in canonical:
            self.assertIn(f"{name}/SKILL.md", output)
            self.assertIn(f"{name}/_shared/AGENTS.md", output)
            self.assertIn(
                b"GENERATED PORTABLE SKILL",
                output[f"{name}/SKILL.md"],
            )

    def test_portable_markdown_links_resolve_inside_each_bundle(self):
        output = PORTABLE.render()
        PORTABLE.validate_links(output)

        for relative, data in output.items():
            path = Path(relative)
            if path.suffix.lower() != ".md":
                continue
            if path.name == PORTABLE.README:
                continue
            bundle = path.parts[0] if path.parts else None
            if bundle == PORTABLE.MANIFEST:
                continue
            text = data.decode("utf-8")
            for match in PORTABLE.LINK.finditer(text):
                raw = match.group("target").strip().split(maxsplit=1)[0]
                if not raw or raw.startswith(
                    ("#", "http:", "https:", "mailto:", "data:", "/")
                ):
                    continue
                parsed = urlsplit(raw)
                normalized = Path(
                    os.path.normpath(
                        (path.parent / unquote(parsed.path)).as_posix()
                    )
                )
                self.assertTrue(
                    normalized.parts
                    and normalized.parts[0] == bundle,
                    f"{relative} escapes its portable bundle via {raw}",
                )

    def test_committed_distribution_is_byte_exact(self):
        expected = PORTABLE.render()
        self.assertEqual(PORTABLE.drift(expected), [])

    def test_skills_directory_keeps_canonical_source_explicit(self):
        readme = (REPO / "skills/README.md").read_text(encoding="utf-8")
        self.assertIn(".agents/skills/", readme)
        self.assertIn("generated", readme.lower())
        self.assertIn("npx skills", readme)


if __name__ == "__main__":
    unittest.main()
