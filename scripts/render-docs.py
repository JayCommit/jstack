#!/usr/bin/env python3
"""Build the generated docs pages from the skill pack.

The catalog, the writing guide, and the day-to-day guide are written on
each run. Skill bodies stay in skills/. This script does not copy them.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
GROUPS = (
    ("principle", "Principles"),
    ("terraform", "Terraform"),
    ("azure", "Azure"),
    ("aws", "AWS"),
    ("pipelines", "Pipelines"),
    ("github", "GitHub"),
    ("azuredevops", "Azure DevOps"),
    ("servicenow", "ServiceNow"),
    ("k8s", "Kubernetes"),
    ("gitops", "GitOps"),
    ("policy", "Policy"),
    ("ops", "Operations"),
)
BLOB = "https://github.com/JayCommit/jstack/blob/main"


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fields: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if not line.strip() or line.strip().startswith("#"):
            continue
        key, sep, raw = line.partition(":")
        if not sep:
            continue
        fields[key.strip()] = unquote(raw.strip())
    return fields


def unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def load_skills(skills_dir: Path) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    if not skills_dir.is_dir():
        raise SystemExit(f"skills directory not found: {skills_dir}")
    for folder in sorted(path for path in skills_dir.iterdir() if path.is_dir()):
        skill = folder / "SKILL.md"
        if not skill.is_file():
            raise SystemExit(f"{folder.name}: missing SKILL.md")
        fields = parse_frontmatter(skill.read_text(encoding="utf-8"))
        name = fields.get("name", "")
        description = fields.get("description", "")
        if name != folder.name:
            raise SystemExit(
                f"{folder.name}: name '{name}' does not match the folder"
            )
        if not description:
            raise SystemExit(f"{folder.name}: missing description")
        found.append(
            {
                "name": name,
                "description": description,
                "group": name.split("-", 1)[0],
            }
        )
    if not found:
        raise SystemExit(f"no skills under {skills_dir}")
    return found


def catalog_markdown(skills: list[dict[str, str]]) -> str:
    by_group: dict[str, list[dict[str, str]]] = {}
    for skill in skills:
        by_group.setdefault(skill["group"], []).append(skill)
    lines = [
        "# Skills",
        "",
        "Generated from `skills/*/SKILL.md` on each build. "
        "The name and the description are the frontmatter. "
        "The playbook stays in the repository.",
        "",
        f"{len(skills)} skills.",
        "",
    ]
    known = {key for key, _title in GROUPS}
    for key, title in GROUPS:
        rows = by_group.get(key, [])
        if not rows:
            continue
        lines.extend(section(title, rows))
    modes = [skill for skill in skills if skill["group"] not in known]
    if modes:
        lines.extend(section("Modes", modes))
    lines.extend(
        [
            "## Still open",
            "",
            "The areas above are in the repository. "
            "Live trials in Cursor, GitHub Copilot, and Claude Code are still open, "
            "and the `v0.1.0` tag is not cut. "
            "That work is [issue 1](https://github.com/JayCommit/jstack/issues/1).",
            "",
        ]
    )
    return "\n".join(lines)


def section(title: str, rows: list[dict[str, str]]) -> list[str]:
    lines = [f"## {title}", ""]
    for skill in sorted(rows, key=lambda item: item["name"]):
        url = f"{BLOB}/skills/{skill['name']}/SKILL.md"
        lines.append(f"### {skill['name']}")
        lines.append("")
        lines.append(skill["description"])
        lines.append("")
        lines.append(f"[Read {skill['name']}]({url})")
        lines.append("")
    return lines


def rewrite(text: str, pairs: tuple[tuple[str, str], ...]) -> str:
    for old, new in pairs:
        text = text.replace(old, new)
    return text


def copy_guide(source: Path, dest: Path, pairs: tuple[tuple[str, str], ...]) -> None:
    if not source.is_file():
        raise SystemExit(f"missing guide: {source}")
    body = rewrite(source.read_text(encoding="utf-8"), pairs)
    note = (
        f"<!-- Copied from {source.as_posix()} by scripts/render-docs.py. "
        "Edit that file. -->\n\n"
    )
    dest.write_text(note + body, encoding="utf-8", newline="\n")


def render(repo: Path, skills_dir: Path, out_dir: Path, skip_lint: bool) -> None:
    if not skip_lint:
        lint = repo / "scripts" / "lint-skills"
        result = subprocess.run(
            [sys.executable, str(lint), str(skills_dir)],
            cwd=repo,
            check=False,
        )
        if result.returncode != 0:
            raise SystemExit(result.returncode)
    out_dir.mkdir(parents=True, exist_ok=True)
    skills = load_skills(skills_dir)
    (out_dir / "catalog.md").write_text(
        catalog_markdown(skills), encoding="utf-8", newline="\n"
    )
    copy_guide(
        repo / "docs" / "writing-skills.md",
        out_dir / "writing-a-skill.md",
        (
            (
                "](templates/SKILL.md)",
                f"]({BLOB}/docs/templates/SKILL.md)",
            ),
            ("](operator-guide.md)", "](day-to-day.md)"),
            (
                "](../examples/jstack-review/README.md)",
                f"]({BLOB}/examples/jstack-review/README.md)",
            ),
        ),
    )
    copy_guide(
        repo / "docs" / "operator-guide.md",
        out_dir / "day-to-day.md",
        (("](writing-skills.md)", "](writing-a-skill.md)"),),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills", type=Path, default=REPO / "skills")
    parser.add_argument("--out", type=Path, default=REPO / "site")
    parser.add_argument("--skip-lint", action="store_true")
    args = parser.parse_args(argv)
    render(REPO, args.skills, args.out, args.skip_lint)
    return 0


if __name__ == "__main__":
    sys.exit(main())
