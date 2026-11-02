# jstack

Jay's DevOps skill pack for AI coding agents, focused on **Azure, AWS and Terraform** and the pipelines that ship them. It's a set of skills, principles and agents for:

- **Terraform:** module design, plan review, state/backends/locking, drift, testing, tflint/checkov/Trivy
- **Azure:** landing zones, RBAC/Entra ID, AKS, Key Vault, networking, Azure DevOps Pipelines, Bicep awareness, cost
- **AWS:** IAM least privilege, Organizations/SCPs, VPC, EKS, ECS, Secrets Manager/SSM, CloudWatch, cost
- **CI/CD:** GitHub Actions and Azure DevOps YAML pipelines, OIDC federation instead of static keys, environments/approvals, reusable workflows and templates, artifacts and releases
- **Platform:** containers, Kubernetes, Helm, GitOps (Argo CD/Flux), policy as code (OPA, Sentinel, Azure Policy), observability
- **Operations:** change safety, secrets, cost, incidents, runbooks and postmortems

**Status:** principles, Terraform, Azure, AWS, pipelines and platform skills are in. Operations playbooks are still open. Specialist agent personas are not written yet. Progress is tracked in [issue #1](../../issues/1).

## Inspiration and credit

jstack is inspired by [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan (MIT licence), part of [cursor/plugins](https://github.com/cursor/plugins). It follows pstack's layout (one folder per skill with a `SKILL.md`, `principle-*` skills, agents and a plugin manifest). The content here is written from scratch for cloud DevOps work and is not copied from pstack.

## One source, many agents

Skills live once in `skills/<name>/SKILL.md` using the open [Agent Skills format](https://agentskills.io/specification): YAML frontmatter with `name` and `description`, then Markdown instructions.

| Tool | How it picks jstack up |
| --- | --- |
| Cursor | Plugin manifest at `.cursor-plugin/plugin.json` (`skills: ./skills/`, `agents: ./agents/`) |
| GitHub Copilot (VS Code, CLI, cloud agent, code review) | `gh skill install JayCommit/jstack` into `~/.copilot/skills` / `.agents/skills`, or `scripts/sync` copies skills into a repo's `.github/skills` |
| Claude Code, Codex, Gemini CLI and other agents | `AGENTS.md` plus `.agents/skills` / `.claude/skills` |

## Layout

```text
.cursor-plugin/plugin.json   Cursor plugin manifest
plugin.json                  Generic agent-plugins manifest
skills/<name>/SKILL.md       Source of truth for every skill and principle
agents/                      Specialist agent personas
docs/                        Guide and per-tool notes
scripts/                     Sync, install and lint helpers
AGENTS.md                    Cross-agent instructions
.github/copilot-instructions.md  Copilot instructions for working on this repo
```

## Tooling

- [`scripts/lint-skills`](scripts/lint-skills) checks `skills/<name>/SKILL.md` for frontmatter, naming, placeholders and relative links. The style guide is [Writing skills](docs/writing-skills.md).
- [`scripts/sync`](scripts/sync) (and [`scripts/sync.ps1`](scripts/sync.ps1)) copies skills into another repo. It prints `create`, `update` or `unchanged` per skill. `--dry-run` changes nothing.

```bash
scripts/lint-skills
scripts/sync --all /path/to/target-repo
scripts/sync --target-dir .agents/skills 'terraform-*' /path/to/target-repo
scripts/sync --dry-run --all /path/to/target-repo
```

```powershell
./scripts/sync.ps1 -All -Target /path/to/target-repo
./scripts/sync.ps1 -Skill terraform-* -TargetDir .agents/skills -Target /path/to/target-repo
```

## Licence

MIT. See [LICENSE](LICENSE).
