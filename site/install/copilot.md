# GitHub Copilot

The repository is private. `gh skill install` works for an account that can read it.

## On your machine

`--all` installs every skill. `--scope user` keeps the copy out of the current repository. Without `--all` or a skill name, a non-interactive run only lists skills.

```bash
gh skill install JayCommit/jstack --all --scope user --agent github-copilot
```

Pass one skill name instead of `--all` when the machine should not get the whole pack.

Prove the install by listing what that agent can see:

```bash
gh skill list --scope user --agent github-copilot
```

The skills you named are in that list. There is no separate uninstall command. [Remove](remove.md) deletes the directory the list prints.

## In one repository

`scripts/sync` copies skills into the target. The default destination is `.github/skills`. The first dry run prints `create`. After the copy, the same dry run prints `unchanged`. A dry run changes nothing.

<!-- markdownlint-disable MD046 -->

=== "Bash"

    ```bash
    scripts/sync --dry-run --all /path/to/target-repo
    scripts/sync --all /path/to/target-repo
    scripts/sync --target-dir .agents/skills 'terraform-*' 'principle-*' /path/to/target-repo
    ```

=== "PowerShell"

    PowerShell 7. The script stops on Windows PowerShell 5.1.

    ```powershell
    ./scripts/sync.ps1 -DryRun -All -Target /path/to/target-repo
    ./scripts/sync.ps1 -All -Target /path/to/target-repo
    ./scripts/sync.ps1 -Skill terraform-* -TargetDir .agents/skills -Target /path/to/target-repo
    ```

<!-- markdownlint-enable MD046 -->

Run the same dry run again after the copy. It prints `unchanged` for each skill in the scope.

## Personas and prompts

`scripts/sync` does not copy personas, slash prompts, or path rules. Copy `agents/*.md` to the target's `.github/agents/` when that repository should offer the personas. Copy `.github/prompts/*.prompt.md` and `.github/instructions/*.instructions.md` when it should offer `/plan-review`, `/pipeline-review`, `/postmortem`, `/runbook`, and the path rules.

Change `agents/` in this repository first, then copy again. The files under `.github/agents/` match `agents/`.
