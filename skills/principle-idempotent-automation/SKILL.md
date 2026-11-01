---
name: principle-idempotent-automation
description: "Apply when writing or rerunning Terraform, scripts, GitHub Actions or Azure DevOps pipelines. A second run with the same inputs must succeed, change nothing further and be safe to start twice."
license: MIT
---

# Idempotent automation

Running the automation again with the same inputs must converge. The second run succeeds and changes nothing.

## Use when

- You write or change Terraform, a shell or PowerShell script, a GitHub Actions workflow or an Azure DevOps pipeline.
- You rerun a failed job or a failed apply.
- A pipeline can be started twice for the same commit.
- A script creates or updates cloud resources.

## Rules

- Apply the saved plan, then plan again with no further edits. The second `terraform plan -detailed-exitcode` should exit 0. If it still reports changes, the configuration is not stable. How the plan was saved is in `principle-change-safety`.
- Scripts create or update. A create call that fails when the resource already exists is unfinished. In Bash, start with `set -euo pipefail` and test the condition you branch on.
- Give each production apply a GitHub Actions `concurrency` group per environment and state key. Leave `cancel-in-progress` false so a second run waits instead of killing an apply.
- An Azure DevOps deployment stage must succeed when it is rerun after a failure halfway through. A task that only works against an empty resource group is not finished.
- Keep resource names stable across runs. A name taken from the clock or a random suffix creates a new resource each time.
- Rerun the same commit. A partial apply that needs a fresh plan is a new change and goes through review again.
- A retry still runs the checks the first attempt already passed. Skipping them hides a half-applied result.

## Red flags

- The second run fails because the resource already exists.
- Two production applies can run at the same time against one state file.
- Resource names change on every pipeline run.
- A script appends a rule, a tag or a permission without reading what is already there.
- Rerunning a green pipeline produces another diff.

## Done when

- A second run with the same inputs exits successfully and changes nothing.
- Production applies for one state or environment are serialised.
- A failed run can be rerun and reaches the same end state.
