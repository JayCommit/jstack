# Other agents

Claude Code, Codex, Gemini CLI, and other agents that read `AGENTS.md` use that file plus a skill directory. Do not keep a second copy of the skill text by hand.

Point the agent at `AGENTS.md` in the repository you want it to work in. Sync the skills you chose into `.agents/skills` or `.claude/skills`.

<!-- markdownlint-disable MD046 -->

=== "Bash"

    ```bash
    scripts/sync --dry-run --target-dir .agents/skills --all /path/to/target-repo
    scripts/sync --target-dir .agents/skills --all /path/to/target-repo
    scripts/sync --dry-run --target-dir .claude/skills 'azure-*' 'principle-*' /path/to/target-repo
    ```

=== "PowerShell"

    ```powershell
    ./scripts/sync.ps1 -DryRun -All -TargetDir .agents/skills -Target /path/to/target-repo
    ./scripts/sync.ps1 -All -TargetDir .agents/skills -Target /path/to/target-repo
    ```

<!-- markdownlint-enable MD046 -->

The dry run after the copy prints `unchanged`.

A machine install for one of these agents uses the same `gh skill install` command as Copilot, with `--agent` set to that host and `--scope user`. List it back with `gh skill list --scope user --agent <agent>`.
