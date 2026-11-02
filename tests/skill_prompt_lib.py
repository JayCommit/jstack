"""Build the example asks that sit beside each skill.

Ask 1 records the first step or rule. Ask 2 records the next one.
The files are fixtures. They are not a live trial.
"""

from __future__ import annotations

import re
from pathlib import Path

NUMBERED = re.compile(r"^(\d+)\. (.*)$")


def section(text: str, title: str) -> str:
    match = re.search(rf"^## {re.escape(title)}\s*$", text, re.MULTILINE)
    if not match:
        return ""
    rest = text[match.end() :]
    nxt = re.search(r"^## ", rest, re.MULTILINE)
    return rest[: nxt.start()] if nxt else rest


def bullets(body: str) -> list[str]:
    found = []
    in_fence = False
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not stripped.startswith("- "):
            continue
        found.append(stripped[2:].strip())
    return found


def numbered_steps(body: str) -> list[str]:
    blocks: list[list[str]] = []
    current: list[str] | None = None
    in_fence = False
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            if current is not None and current[-1] != "":
                current.append("")
            continue
        if in_fence:
            continue
        match = NUMBERED.match(line)
        if match:
            if current is not None:
                blocks.append(current)
            current = [match.group(2).strip()]
            continue
        if current is None:
            continue
        if current[-1] == "":
            continue
        if stripped == "" or stripped.startswith("|"):
            current.append("")
            continue
        current.append(stripped)
    if current is not None:
        blocks.append(current)
    steps = []
    for block in blocks:
        parts = []
        for part in block:
            if part == "":
                break
            parts.append(part)
        text = " ".join(parts).strip()
        if text:
            steps.append(text)
    return steps


def as_ask(bullet: str) -> str:
    if bullet.startswith("You "):
        return "I " + bullet[4:]
    return bullet


def parse_skill(text: str) -> dict:
    actions = numbered_steps(section(text, "Steps"))
    label = "Step"
    if not actions:
        actions = bullets(section(text, "Rules"))
        label = "Rule"
    checks = bullets(section(text, "Safety checks"))
    check_label = "Check"
    if not checks:
        checks = bullets(section(text, "Red flags"))
        check_label = "Red flag"
    return {
        "use_when": bullets(section(text, "Use when")),
        "actions": actions,
        "label": label,
        "checks": checks,
        "check_label": check_label,
        "dones": bullets(section(text, "Done when")),
    }


def _pick(items: list[str], index: int) -> str:
    if not items:
        raise ValueError("skill section is empty")
    if index < len(items):
        return items[index]
    return items[0]


def _first_sentence(text: str) -> str:
    head, sep, _tail = text.partition(". ")
    if sep:
        return head + "."
    return text


def asks_for(parsed: dict) -> list[str]:
    """Ask 1 is the first trigger. Ask 2 is the next step, so the two cannot record the same action."""
    primary = parsed["use_when"][0] if parsed["use_when"] else _pick(parsed["actions"], 0)
    return [as_ask(primary), _first_sentence(_pick(parsed["actions"], 1))]


def render_prompts(name: str, parsed: dict) -> str:
    ask1, ask2 = asks_for(parsed)
    label = parsed["label"]
    check_label = parsed["check_label"]
    lines = [
        f"# Prompts for {name}",
        "",
        f"Example asks for `{name}`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.",
        "",
        "## Ask 1",
        "",
        ask1,
        "",
        "### Expected for ask 1",
        "",
        f"- Load `{name}` and follow that file through its own done-when.",
        f"- {label}: {_pick(parsed['actions'], 0)}",
        f"- {check_label}: {_pick(parsed['checks'], 0)}",
        f"- Done when: {_pick(parsed['dones'], 0)}",
        "",
        "## Ask 2",
        "",
        ask2,
        "",
        "### Expected for ask 2",
        "",
        f"- Load `{name}` and follow that file through its own done-when.",
        f"- {label}: {_pick(parsed['actions'], 1)}",
        f"- {check_label}: {_pick(parsed['checks'], 1)}",
        f"- Done when: {_pick(parsed['dones'], 1)}",
        "",
    ]
    return "\n".join(lines)


def skill_dirs(root: Path) -> list[Path]:
    skills = root / "skills"
    return sorted(
        path
        for path in skills.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    )
