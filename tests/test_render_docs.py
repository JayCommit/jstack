#!/usr/bin/env python3
"""The docs render lists frontmatter and does not paste skill bodies."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "render_docs", ROOT / "scripts" / "render-docs.py"
)
assert SPEC is not None and SPEC.loader is not None
render_docs = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(render_docs)


class RenderDocsTest(unittest.TestCase):
    def test_catalog_lists_frontmatter_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            render_docs.render(ROOT, ROOT / "skills", out, skip_lint=True)
            catalog = (out / "catalog.md").read_text(encoding="utf-8")
            self.assertIn("### terraform-plan-review", catalog)
            self.assertIn("### jay-mode", catalog)
            self.assertIn("## Modes", catalog)
            self.assertNotIn("## Safety checks", catalog)
            self.assertIn("issue 1", catalog)
            day = (out / "day-to-day.md").read_text(encoding="utf-8")
            self.assertIn("](writing-a-skill.md)", day)
            self.assertNotIn("](writing-skills.md)", day)
            writing = (out / "writing-a-skill.md").read_text(encoding="utf-8")
            self.assertIn("/docs/templates/SKILL.md)", writing)
            self.assertIn("](day-to-day.md)", writing)
            self.assertNotIn("](operator-guide.md)", writing)

    def test_name_mismatch_exits(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "ops-example"
            folder.mkdir()
            (folder / "SKILL.md").write_text(
                "---\nname: other\ndescription: A mismatched name.\n---\n",
                encoding="utf-8",
            )
            with self.assertRaises(SystemExit):
                render_docs.load_skills(Path(tmp))


if __name__ == "__main__":
    unittest.main()
