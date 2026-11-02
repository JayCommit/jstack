"""Every skill ships example asks, and ask 2 records a later step."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))

from skill_prompt_lib import parse_skill, render_prompts, skill_dirs  # noqa: E402


class PromptFilesTest(unittest.TestCase):
    def test_every_skill_has_prompts(self):
        dirs = skill_dirs(ROOT)
        self.assertGreaterEqual(len(dirs), 54)
        problems = []
        for skill_dir in dirs:
            prompts = skill_dir / "tests" / "prompts.md"
            if not prompts.is_file():
                problems.append(f"{skill_dir.name}: missing prompts.md")
                continue
            skill = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            parsed = parse_skill(skill)
            expected = render_prompts(skill_dir.name, parsed)
            actual = prompts.read_text(encoding="utf-8")
            if actual != expected:
                problems.append(f"{skill_dir.name}: prompts.md does not match the skill")
                continue
            if len(parsed["actions"]) < 2:
                problems.append(f"{skill_dir.name}: needs a second step or rule")
                continue
            action_lines = [
                line
                for line in actual.splitlines()
                if line.startswith("- Step: ") or line.startswith("- Rule: ")
            ]
            if len(action_lines) != 2 or action_lines[0] == action_lines[1]:
                problems.append(f"{skill_dir.name}: ask 2 repeats the first step")
            ask2 = actual.split("## Ask 2", 1)[1]
            if parsed["actions"][1] not in ask2:
                problems.append(f"{skill_dir.name}: ask 2 omits the second step")
        self.assertEqual(problems, [])


if __name__ == "__main__":
    unittest.main()
