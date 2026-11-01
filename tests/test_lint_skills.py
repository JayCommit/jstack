#!/usr/bin/env python3
"""Black-box tests for scripts/lint-skills."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "lint-skills"
GOOD = ROOT / "tests" / "lint-skills" / "fixtures" / "good" / "skills"
BAD = ROOT / "tests" / "lint-skills" / "fixtures" / "bad" / "skills"

DESCRIPTION = (
    "Valid description used by the linter tests. "
    "It is long enough to satisfy the fifty character minimum."
)


def run_lint(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(SCRIPT), *args],
        cwd=cwd or ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def write_skill(
    skills_root: Path,
    folder: str,
    description: str = DESCRIPTION,
    body: str = "## Done when\n\n- Ready.\n",
    name: str | None = None,
    frontmatter: bool = True,
    extra_frontmatter: str = "",
) -> Path:
    skill_dir = skills_root / folder
    skill_dir.mkdir(parents=True, exist_ok=True)
    skill_name = folder if name is None else name
    if frontmatter:
        text = (
            "---\n"
            f"name: {skill_name}\n"
            f'description: "{description}"\n'
            f"{extra_frontmatter}"
            "---\n"
            "\n"
            f"# {skill_name}\n"
            "\n"
            f"{body}"
        )
    else:
        text = body
    path = skill_dir / "SKILL.md"
    path.write_text(text, encoding="utf-8")
    return path


class LintSkillsTests(unittest.TestCase):
    def test_help(self) -> None:
        result = run_lint("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("usage", result.stdout.lower())

    def test_good_fixture(self) -> None:
        result = run_lint(str(GOOD))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("error:", result.stdout)
        self.assertNotIn("warning:", result.stdout)

    def test_bad_fixtures(self) -> None:
        cases = {
            "ops-name-mismatch": "name 'ops-other' does not match folder 'ops-name-mismatch'",
            "ops-short-description": "description is",
            "ops-no-frontmatter": "missing YAML frontmatter",
            "ops-aws-key": "possible AWS access key ID",
            "ops-broken-link": "broken relative link 'does-not-exist.md'",
        }
        for folder, message in cases.items():
            with self.subTest(folder=folder):
                skill = BAD / folder
                result = run_lint(str(skill))
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn(message, result.stdout)
                self.assertRegex(result.stdout, r":\d+: error:")

    def test_aws_key_line_number(self) -> None:
        skill = BAD / "ops-aws-key" / "SKILL.md"
        line_no = next(
            number
            for number, line in enumerate(skill.read_text(encoding="utf-8").splitlines(), start=1)
            if "AKIA" in line
        )
        result = run_lint(str(skill))
        self.assertEqual(result.returncode, 1)
        self.assertIn(f":{line_no}: error: possible AWS access key ID", result.stdout)

    def test_repo_skills(self) -> None:
        result = run_lint()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("error:", result.stdout)
        self.assertIn("0 error(s)", result.stdout)

    def test_repo_skills_from_other_directory(self) -> None:
        result = run_lint(cwd=Path(tempfile.gettempdir()))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("error:", result.stdout)

    def test_missing_skill_md(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "skills"
            (root / "ops-empty").mkdir(parents=True)
            result = run_lint(str(root))
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("missing SKILL.md", result.stdout)

    def test_warnings_do_not_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "skills"
            write_skill(root, "custom-example")
            warned = run_lint(str(root / "custom-example"))
            write_skill(root, "ops-no-done", body="## Steps\n\n1. Stop.\n")
            missing_done = run_lint(str(root / "ops-no-done"))
            write_skill(root, "principle-short", body="Keep the change small.\n")
            principle = run_lint(str(root / "principle-short"))
        self.assertEqual(warned.returncode, 0, warned.stdout)
        self.assertIn("does not use a known area prefix", warned.stdout)
        self.assertEqual(missing_done.returncode, 0, missing_done.stdout)
        self.assertIn("missing 'Done when' heading", missing_done.stdout)
        self.assertEqual(principle.returncode, 0, principle.stdout)
        self.assertNotIn("warning:", principle.stdout)

    def test_placeholders_allowed(self) -> None:
        body = "\n".join(
            (
                "## Done when",
                "",
                "- Ready.",
                "",
                "00000000-0000-0000-0000-000000000000",
                "11111111-1111-1111-1111-111111111111",
                "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                "123456789012",
                "000000000000",
                "999999999999",
                "10.1.2.3",
                "172.16.0.1",
                "172.31.255.255",
                "192.168.1.1",
                "127.0.0.1",
                "0.0.0.0",
                "192.0.2.10",
                "198.51.100.4",
                "203.0.113.9",
                "",
            )
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "skills"
            write_skill(root, "ops-placeholders", body=body)
            result = run_lint(str(root))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("error:", result.stdout)

    def test_secrets_and_ids_flagged(self) -> None:
        access_key = "AKIA" + "ABCDEFGHIJKLMNOP"
        github = "ghp_" + ("a" * 36)
        slack = "xoxb-" + ("1" * 12)
        quoted = "password" + ' = "' + ("x" * 12) + '"'
        private_key = "-----BEGIN " + "RSA PRIVATE KEY-----"
        guid = "12345678-1234-1234-1234-123456789abc"
        account = "210987" + "654321"
        body = "\n".join(
            (
                "## Done when",
                "",
                "- Ready.",
                "",
                access_key,
                private_key,
                github,
                slack,
                quoted,
                guid,
                account,
                "8.8.8.8",
                "172.15.0.1",
                "0.0.0.1",
                "",
            )
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "skills"
            write_skill(root, "ops-leaks", body=body)
            result = run_lint(str(root))
        self.assertEqual(result.returncode, 1, result.stdout)
        for message in (
            "possible AWS access key ID",
            "possible private key",
            "possible GitHub token",
            "possible Slack token",
            "possible hardcoded secret",
            "possible real GUID",
            "possible AWS account ID",
            "possible public IPv4 address",
        ):
            self.assertIn(message, result.stdout)

    def test_fenced_link_ignored_and_real_link_resolves(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "skills"
            skill = write_skill(
                root,
                "ops-links",
                body=(
                    "See [notes](notes.md).\n"
                    "\n"
                    "```text\n"
                    "See [missing](missing.md).\n"
                    "```\n"
                    "\n"
                    "## Done when\n"
                    "\n"
                    "- Ready.\n"
                ),
            )
            (skill.parent / "notes.md").write_text("notes\n", encoding="utf-8")
            ok = run_lint(str(skill))
            (skill.parent / "notes.md").unlink()
            broken = run_lint(str(skill))
        self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)
        self.assertEqual(broken.returncode, 1, broken.stdout)
        self.assertIn("broken relative link 'notes.md'", broken.stdout)
        self.assertNotIn("missing.md", broken.stdout)

    def test_description_bounds_and_scalars(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "skills"
            write_skill(root, "ops-min", description="a" * 50)
            minimum = run_lint(str(root / "ops-min"))
            write_skill(root, "ops-short", description="a" * 49)
            short = run_lint(str(root / "ops-short"))
            write_skill(root, "ops-max", description="a" * 1024)
            maximum = run_lint(str(root / "ops-max"))
            write_skill(root, "ops-long", description="a" * 1025)
            long = run_lint(str(root / "ops-long"))
            bare = root / "ops-bare"
            bare.mkdir(parents=True)
            (bare / "SKILL.md").write_text(
                "---\n"
                "name: ops-bare\n"
                "description: Use this when planning: it is definitely long enough for the linter.\n"
                "---\n"
                "\n"
                "# Bare\n"
                "\n"
                "## Done when\n"
                "\n"
                "- Ready.\n",
                encoding="utf-8",
            )
            bare_result = run_lint(str(bare))
            quoted = root / "ops-quoted"
            quoted.mkdir(parents=True)
            (quoted / "SKILL.md").write_text(
                "---\n"
                "name: ops-quoted\n"
                "description: 'A single quoted description that is definitely long enough for the linter to accept.'\n"
                "---\n"
                "\n"
                "# Quoted\n"
                "\n"
                "## Done when\n"
                "\n"
                "- Ready.\n",
                encoding="utf-8",
            )
            quoted_result = run_lint(str(quoted))
        self.assertEqual(minimum.returncode, 0, minimum.stdout)
        self.assertEqual(maximum.returncode, 0, maximum.stdout)
        self.assertEqual(short.returncode, 1)
        self.assertIn("description is 49 characters", short.stdout)
        self.assertEqual(long.returncode, 1)
        self.assertIn("description is 1025 characters", long.stdout)
        self.assertEqual(bare_result.returncode, 0, bare_result.stdout)
        self.assertEqual(quoted_result.returncode, 0, quoted_result.stdout)

    def test_bad_name_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "skills"
            long_name = "ops-" + ("a" * 61)
            write_skill(root, long_name)
            too_long = run_lint(str(root / long_name))
            write_skill(root, "ops-bad", name="Ops-Bad")
            bad_chars = run_lint(str(root / "ops-bad"))
        self.assertEqual(too_long.returncode, 1)
        self.assertIn("maximum is 64", too_long.stdout)
        self.assertEqual(bad_chars.returncode, 1)
        self.assertIn("name must match ^[a-z0-9]+(-[a-z0-9]+)*$", bad_chars.stdout)


if __name__ == "__main__":
    unittest.main()
