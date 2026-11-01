# jstack

Jay's DevOps skill pack for AI coding agents. It's a set of skills, principles and agents for infrastructure and operations work: IaC, CI/CD, containers, Proxmox/Linux/Windows Server ops, incident response and change safety.

**Status:** scaffold only. Progress is tracked in [issue #1](../../issues/1).

## Inspiration and credit

jstack is inspired by [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan (MIT licence), part of [cursor/plugins](https://github.com/cursor/plugins). It follows pstack's layout (one folder per skill with a `SKILL.md`, `principle-*` skills, agents and a plugin manifest). The content here is written from scratch for DevOps work and is not copied from pstack.

## One source, many agents

Skills live once in `skills/<name>/SKILL.md` using the open [Agent Skills format](https://agentskills.io/specification): YAML frontmatter with `name` and `description`, then Markdown instructions.

| Tool | How it picks jstack up |
| --- | --- |
| Cursor | Plugin manifest at `.cursor-plugin/plugin.json` (`skills: ./skills/`, `agents: ./agents/`) |
| GitHub Copilot (VS Code, CLI, cloud agent, code review) | `gh skill install JayCommit/jstack` into `~/.copilot/skills` / `.agents/skills`, or `scripts/sync` copies skills into a repo's `.github/skills` |
| Claude Code, Codex, Gemini CLI and other agents | `AGENTS.md` plus `.agents/skills` / `.claude/skills` |

## Layout

```
.cursor-plugin/plugin.json   Cursor plugin manifest
plugin.json                  Generic agent-plugins manifest
skills/<name>/SKILL.md       Source of truth for every skill and principle
agents/                      Specialist agent personas
docs/                        Guide and per-tool notes
scripts/                     Sync, install and lint helpers
AGENTS.md                    Cross-agent instructions
.github/copilot-instructions.md  Copilot instructions for working on this repo
```

## Licence

MIT. See [LICENSE](LICENSE).
