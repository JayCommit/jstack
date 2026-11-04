# jstack

Jay's DevOps skill pack for AI coding agents, focused on **Azure, AWS and Terraform** and the pipelines that ship them. It's a set of skills, principles and agents for:

- **Terraform:** module design, plan review, state/backends/locking, drift, testing, tflint/checkov/Trivy
- **Azure:** landing zones, RBAC/Entra ID, AKS, Key Vault, networking, Azure DevOps Pipelines, Bicep awareness, cost
- **AWS:** IAM least privilege, Organizations/SCPs, VPC, EKS, ECS, Secrets Manager/SSM, CloudWatch, cost
- **CI/CD:** GitHub Actions and Azure DevOps YAML pipelines, OIDC federation instead of static keys, environments/approvals, reusable workflows and templates, artifacts and releases, runner and agent-pool hardening
- **Repositories:** GitHub repositories and pull requests, Azure DevOps Git repositories, branch policy, and required reviewers
- **ServiceNow:** the signed-in user's incidents, problems, changes, and catalog requests
- **Platform:** containers, Kubernetes, Helm, GitOps (Argo CD/Flux), policy as code (OPA, Sentinel, Azure Policy), observability
- **Operations:** change safety, secrets, cost, incidents, runbooks, postmortems, backup and restore, access reviews, certificates

**Status:** principles (including stop-at-approval and the resource baseline), Terraform, Azure, AWS, pipelines, GitHub and Azure DevOps repositories, ServiceNow, platform, operations, `jay-mode`, `setup-jstack`, and the four specialist agents are in. The sample stack is `examples/jstack-sample`. The blinded review target is `examples/jstack-review`. The task guide is [Operator guide](docs/operator-guide.md). Live trials in Cursor, Copilot, and Claude Code are still open, and the repository is still `0.0.1`. Progress is tracked in [issue #1](../../issues/1).

## Inspiration and credit

jstack is inspired by [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan (MIT licence), part of [cursor/plugins](https://github.com/cursor/plugins). It follows pstack's layout (one folder per skill with a `SKILL.md`, `principle-*` skills, agents and a plugin manifest). The content here is written from scratch for cloud DevOps work and is not copied from pstack.

## One source, many agents

Skills live once in `skills/<name>/SKILL.md` using the open [Agent Skills format](https://agentskills.io/specification): YAML frontmatter with `name` and `description`, then Markdown instructions.

| Tool | How it picks jstack up |
| --- | --- |
| Cursor | Plugin manifest at `.cursor-plugin/plugin.json` (`skills: ./skills/`, `agents: ./agents/`) |
| GitHub Copilot (VS Code, CLI, cloud agent, code review) | `gh skill install JayCommit/jstack --all --scope user --agent github-copilot`, or `scripts/sync` into a repo. Follow `setup-jstack`. |
| Claude Code, Codex, Gemini CLI and other agents | `AGENTS.md` plus `.agents/skills` / `.claude/skills` |

## Layout

```text
.cursor-plugin/plugin.json   Cursor plugin manifest
plugin.json                  Generic agent-plugins manifest
skills/<name>/SKILL.md       Source of truth for every skill and principle
agents/                      Specialist agent personas (copied to .github/agents)
.github/prompts/             Copilot slash prompts
.github/instructions/        Copilot path rules
examples/jstack-sample/      Fixture stack. Nothing in it is applied.
examples/jstack-review/      Blinded plan and workflow review. Not a pattern.
docs/                        Operator guide, author guide, and templates
site/                        Docs site source. Catalog pages are generated
mkdocs.yml                   MkDocs Material config. HTML builds to site-dist/
scripts/                     Sync, install, lint, and docs render helpers
AGENTS.md                    Cross-agent instructions
.github/copilot-instructions.md  Copilot instructions for working on this repo
```

## Tooling

- [`scripts/lint-skills`](scripts/lint-skills) checks `skills/<name>/SKILL.md` for frontmatter, naming, placeholders, relative links, and a Safety checks line that names `principle-stop-at-approval`. The style guide is [Writing skills](docs/writing-skills.md). The task guide is [Operator guide](docs/operator-guide.md).
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

## Docs site

The guide for install, day-to-day use, and removal lives in `site/`. `scripts/render-docs.py` writes `site/catalog.md` from skill frontmatter and copies the operator guide and the writing guide. Those generated pages are not committed. `mkdocs build` writes HTML to `site-dist/`, which is not committed.

```bash
python -m pip install -r requirements-docs.txt
python scripts/render-docs.py
python -m mkdocs build --strict
```

Open `site-dist/index.html`. The public Pages URL stays off until the visibility choice is recorded on [issue #5](https://github.com/JayCommit/jstack/issues/5). Publishing stays off while the repository is private, because a Pages site on the current plan is public.

## Licence

MIT. See [LICENSE](LICENSE).
