---
name: setup-jstack
description: "Use when you install jstack for Cursor, GitHub Copilot, or Claude Code. Sync only the skills that machine or repository needs, and prove the copy with a dry run."
license: MIT
---

# Set up jstack

Install from this repository. Do not paste skills into a chat. Choose the tool, then choose how much of the pack that repo needs.

## Use when

- You install jstack on a machine or into a repository.
- Cursor, Copilot, or Claude Code cannot see the skills.
- A repo should get Terraform skills and not the whole pack.
- You are about to copy a skill by hand.

## Steps

1. Decide the tool and the scope. The scope is the whole pack, or a glob such as `terraform-*`, `azure-*`, `aws-*`, `pipelines-*`, `k8s-*`, `gitops-*`, `policy-*`, `ops-*`, or `principle-*`. A repository that has no cluster does not need the Kubernetes skills. Write the choice down.

2. Cursor uses the plugin. The manifest is `.cursor-plugin/plugin.json`. It points `skills` at `./skills/` and `agents` at `./agents/`. Install the plugin from this repository. Do not also copy the same skills into the project.

3. Copilot on a machine installs the pack for that user. `--all` installs every skill. `--scope user` keeps the copy out of the current repository. Without `--all` or a skill name, a non-interactive run only lists skills.

   ```bash
   gh skill install JayCommit/jstack --all --scope user --agent github-copilot
   ```

   Pass one skill name instead of `--all` when the machine should not get the whole pack. For one repository, copy from this repo with `scripts/sync`. The default destination is `.github/skills`. The first dry run prints `create`. After the copy, the same dry run prints `unchanged`.

   ```bash
   scripts/sync --dry-run --all /path/to/target-repo
   scripts/sync --all /path/to/target-repo
   scripts/sync --target-dir .agents/skills 'terraform-*' 'principle-*' /path/to/target-repo
   ```

   On Windows, run `scripts/sync.ps1` with PowerShell 7. It requires version 7 and stops on Windows PowerShell 5.1. The parameters are `-DryRun`, `-All`, `-Skill`, `-TargetDir`, and `-Target`.

   ```powershell
   ./scripts/sync.ps1 -DryRun -All -Target /path/to/target-repo
   ```

4. Copilot personas, prompts, and path rules do not ride along with `scripts/sync`. Copy `agents/*.md` to the target's `.github/agents/` when that repo should offer the personas. Copy `.github/prompts/*.prompt.md` and `.github/instructions/*.instructions.md` when that repo should offer `/plan-review`, `/pipeline-review`, `/postmortem`, `/runbook`, and the path rules. The copies in this repo match `agents/`. Change `agents/` first, then copy again.

5. Claude Code, Codex, and other agents that read `AGENTS.md` use that file plus a skill directory. Sync into `.agents/skills` or `.claude/skills` with `--target-dir`. Do not maintain a second copy of the skill text.

6. Prove a repository copy with `scripts/sync`, not with `gh skill install`. Repeat the dry run from step 3, including the target path and either `--all` or the glob you chose. The first dry run prints `create`. The dry run after the copy prints `unchanged`.

   ```bash
   scripts/sync --dry-run --all /path/to/target-repo
   ```

   Prove a machine install with `gh skill list --scope user --agent github-copilot` and confirm the skills you named are listed. `scripts/lint-skills` passes on this repo. Do not declare the install done because the files were copied.

7. Do not copy secrets, kubeconfigs, or cloud keys into the target. The sample stack under `examples/jstack-sample` is the fixture for a later trial. It is not an install step, and nothing in it is applied by this skill.

## Safety checks

- The tool and the skill glob are named before the copy.
- Cursor is the plugin, or the sync, not both for the same skills.
- A repository copy was dry-run first. The dry run after the copy prints `unchanged`.
- Personas and prompts were copied only when that repo should have them.
- No secret was added to the target.

## Rollback

Delete the skill directory the sync created, or uninstall the Cursor plugin. Do not delete unrelated skills in the target. A bad glob is fixed by deleting that directory and syncing the glob you meant. Follow `principle-rollback-first` only when the sync landed in a repository that deploys production. The copy itself does not change Azure or AWS.

## Done when

- The chosen tool can see the skills in the scope you named.
- A second dry run reports `unchanged` for each of those skills.
- Agents, prompts, and path instructions are present only where you decided to copy them.
