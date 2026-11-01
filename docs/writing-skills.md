# Writing skills

A jstack skill is a Markdown file an agent can load. The source of truth is `skills/<name>/SKILL.md`. This guide is the house style. `scripts/lint-skills` checks the rules that can be checked by machine.

Write new text for this repo. Do not paste text from pstack or other skill packs.

## Frontmatter

The file starts with a YAML block and a closing line of `---`. `scripts/lint-skills` reads simple `key: value` lines only, so keep each value on one line. Quote a value that contains a colon or a hash.

```yaml
---
name: area-skill-name
description: "What this skill does and when to use it."
license: MIT
---
```

Required keys:

- `name` is lowercase words separated by single hyphens, matching `^[a-z0-9]+(-[a-z0-9]+)*$`. It is at most 64 characters and it is the same string as the folder name.
- `description` is 50 to 1024 characters. It says what the skill does and when to use it. The agent uses this text to decide whether to load the skill, so name the trigger, the area and the outcome.

Optional keys:

- `license` records the licence. This repo uses MIT.
- Other keys are allowed. Cursor-only keys such as `disable-model-invocation` are fine. The skill must still make sense to an agent that ignores those keys. Put the real instructions in the body.

## Naming

Prefix the name with the area it belongs to:

| Prefix | Use for |
| --- | --- |
| `terraform-` | Terraform modules, plans, state and testing |
| `azure-` | Azure resources, identity and landing zones |
| `aws-` | AWS accounts, IAM, networking and runtime |
| `pipelines-` | GitHub Actions and Azure DevOps pipelines |
| `k8s-` | Kubernetes workloads and clusters |
| `gitops-` | Argo CD, Flux and other GitOps delivery |
| `policy-` | OPA, Sentinel and Azure Policy |
| `ops-` | Change, incidents, cost, secrets and runbooks |
| `principle-` | Short rules that apply across areas |

A review skill ends with `-review`, for example `terraform-plan-review`.

Two names are allowed without an area prefix: `jay-mode` and `setup-jstack`. Anything else gets a warning from the linter.

## Body

Use these headings, in this order:

1. Use when
2. Steps
3. Safety checks
4. Rollback
5. Done when

Say when the skill applies, what to do, what to check before changing anything, how to undo it, and how to tell it is finished.

A principle (`principle-*`) is a short rule. It may omit Steps and Rollback. Every other skill should include a `Done when` heading. The linter warns if that heading is missing. It does not warn on principles.

Helper files may sit next to `SKILL.md`. A relative Markdown link must point at a file that exists beside the skill. Links inside fenced code blocks are not checked. `http`, `https`, `mailto` and `#anchor` links are left alone.

## Secure defaults

Examples in a skill use:

- OIDC or workload identity federation for Azure and AWS
- least-privilege IAM and RBAC
- pinned provider, module and action versions
- remote state with locking

## Placeholders

Use these placeholders in examples:

- `00000000-0000-0000-0000-000000000000` for a GUID
- `123456789012` for a 12-digit account id
- `example.com` for a hostname

A repeated character (`11111111-1111-1111-1111-111111111111`, `000000000000`) is also treated as a placeholder. Private ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`), loopback (`127.0.0.0/8`), `0.0.0.0`, and the RFC 5737 documentation ranges (`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`) are fine in network examples.

Do not put real secrets, tenant ids, subscription ids, account ids, hostnames or public IP addresses in a skill. The linter reports AWS access key ids, private key blocks, GitHub and Slack tokens, a long quoted password, secret or token, any other GUID, any other 12-digit account id, and any other IPv4 address.

## What the linter reports

Errors fail the run:

- the file does not open with a `---` frontmatter block closed by `---`
- `name` or `description` is missing, or `name` does not match the folder and the pattern above
- `description` is shorter than 50 characters or longer than 1024
- a secret or real id, as above
- a relative Markdown link that does not resolve to a file next to `SKILL.md`
- a folder under the skills directory with no `SKILL.md`

Warnings do not fail the run:

- `name` does not use a known area prefix, and it is not `jay-mode` or `setup-jstack`
- a skill whose name does not start with `principle-` has no `Done when` heading

Run it from the repo root:

```bash
scripts/lint-skills
scripts/lint-skills skills/principle-change-safety/SKILL.md
```

With no path, it checks `skills/` in this repo. Each path you pass is either a skills directory (one subfolder per skill) or a single `SKILL.md`.

## Template

Copy this block into `skills/<name>/SKILL.md`, or start from the file [docs/templates/SKILL.md](templates/SKILL.md). Replace `area-skill-name` with the folder name.

````markdown
---
name: area-skill-name
description: "Replace this with what the skill does and when to use it. Name the trigger, the cloud area and the outcome. Keep it between 50 and 1024 characters."
license: MIT
---

# Area skill title

## Use when

Use this skill when an agent is about to change this area of Azure, AWS, Terraform or the pipeline that ships it. Say which environments and which repositories it covers.

## Steps

1. Read the plan or pipeline diff and list every destroy, replace and permission change.
2. Use OIDC workload identity, pin provider and action versions, and keep state in a remote backend with locking.
3. Apply least-privilege IAM or RBAC. Use placeholders such as `00000000-0000-0000-0000-000000000000`, `123456789012` and `example.com`.
4. Change one thing at a time and promote it through environments after a check.

## Safety checks

- The blast radius is named: subscription, account, cluster and pipeline.
- Examples use federated identity, pinned versions and a locked remote backend.
- Production has a second person to approve it.

## Rollback

Write the rollback before the change. For Terraform, keep the previous state and a plan that reverses this diff. For a pipeline, keep the previous workflow or release definition. Stop if the rollback depends on a step that has not been tried.

## Done when

- The plan or diff matches the requested change and nothing else.
- The safety checks above have been ticked off.
- The change is verified in the target environment, or it has been stopped with the rollback ready.
````
