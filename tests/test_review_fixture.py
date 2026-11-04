#!/usr/bin/env python3
"""The blinded review fixture keeps its planted findings out of the prompt."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "jstack-review"
PROMPTS = (FIXTURE / "prompts.md").read_text(encoding="utf-8")
EXPECTED = (FIXTURE / "expected.md").read_text(encoding="utf-8")
PLAN = (FIXTURE / "terraform" / "plan.txt").read_text(encoding="utf-8")
WORKFLOW = (FIXTURE / ".github" / "workflows" / "deploy.yml").read_text(encoding="utf-8")
SAMPLE = (
    ROOT / "examples" / "jstack-sample" / ".github" / "workflows" / "deploy.yml"
).read_text(encoding="utf-8")

# Strings that would tell the reviewer the answer before they open the fixture.
LEAKS = (
    "destroy",
    "unpinned",
    "static",
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "AZURE_CREDENTIALS",
    "example-access-key",
    "example-secret-key",
    "actions/checkout@v4",
    "azure/login@v2",
    "azurerm_linux_virtual_machine.app",
    "vm-app",
    "contents: write",
    "timeout-minutes",
    "persist-credentials",
)


class ReviewFixtureTests(unittest.TestCase):
    def test_prompt_does_not_name_the_findings(self) -> None:
        lowered = PROMPTS.lower()
        for leak in LEAKS:
            self.assertNotIn(leak.lower(), lowered, leak)
        self.assertNotIn("expected.md", PROMPTS.lower().replace("leave `expected.md` closed", ""))

    def test_plan_plants_one_destroy(self) -> None:
        self.assertIn("azurerm_linux_virtual_machine.app will be destroyed", PLAN)
        self.assertIn("Plan: 0 to add, 0 to change, 1 to destroy.", PLAN)
        self.assertIn("hashicorp/azurerm v4.14.0", PLAN)
        self.assertIn("example-prod.tfstate", PLAN)
        self.assertEqual(PLAN.count("will be destroyed"), 1)

    def test_workflow_plants_unpinned_actions_and_static_keys(self) -> None:
        self.assertIn("uses: actions/checkout@v4", WORKFLOW)
        self.assertIn("uses: azure/login@v2", WORKFLOW)
        self.assertIn("AWS_ACCESS_KEY_ID: example-access-key", WORKFLOW)
        self.assertIn("AWS_SECRET_ACCESS_KEY: example-secret-key", WORKFLOW)
        self.assertIn("secrets.AZURE_CREDENTIALS", WORKFLOW)
        self.assertNotIn("timeout-minutes", WORKFLOW)
        self.assertNotIn("concurrency", WORKFLOW)
        self.assertNotRegex(WORKFLOW, r"AKIA|ASIA|ghp_|github_pat_")
        self.assertNotIn("contents: read", WORKFLOW)

    def test_answer_key_lists_the_planted_findings(self) -> None:
        for needle in (
            "azurerm_linux_virtual_machine.app",
            "will be destroyed",
            "actions/checkout@v4",
            "azure/login@v2",
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
            "example-access-key",
            "example-secret-key",
            "AZURE_CREDENTIALS",
            "timeout-minutes",
            "concurrency",
            "contents: write",
            "persist-credentials: false",
        ):
            self.assertIn(needle, EXPECTED, needle)

    def test_sample_workflow_stays_a_separate_pattern(self) -> None:
        self.assertIn(
            "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
            SAMPLE,
        )
        self.assertNotIn("AWS_SECRET_ACCESS_KEY", SAMPLE)
        self.assertNotIn("@v4", SAMPLE)
        self.assertNotIn("@v2", SAMPLE)
