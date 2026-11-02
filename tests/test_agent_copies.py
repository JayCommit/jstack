"""Copilot agent copies stay identical to agents/."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"
COPILOT = ROOT / ".github" / "agents"


class AgentCopiesTest(unittest.TestCase):
    def test_each_agent_matches_its_copilot_copy(self):
        sources = sorted(AGENTS.glob("*.md"))
        self.assertGreaterEqual(len(sources), 4)
        mismatches = []
        for source in sources:
            copy = COPILOT / source.name
            if not copy.is_file():
                mismatches.append(f"missing {copy.relative_to(ROOT)}")
                continue
            if source.read_bytes() != copy.read_bytes():
                mismatches.append(source.name)
        self.assertEqual(mismatches, [])


if __name__ == "__main__":
    unittest.main()
