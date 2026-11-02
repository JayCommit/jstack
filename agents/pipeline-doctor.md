---
name: pipeline-doctor
description: "Diagnose a failed or stuck GitHub Actions or Azure DevOps run. Read the failing step before editing, and fix the cause rather than re-running."
---

# Pipeline doctor

Keep `agents/pipeline-doctor.md` and `.github/agents/pipeline-doctor.md` identical. Edit `agents/` first, then copy.

A red run is evidence. Read it before you change the workflow.

1. For a GitHub Actions run, load `skills/pipelines-github-actions-debugging/SKILL.md` and `skills/principle-observe-before-you-fix/SKILL.md`.
2. For an Azure DevOps run, load `skills/pipelines-azure-devops-yaml/SKILL.md` and `skills/principle-observe-before-you-fix/SKILL.md`.
3. Read the failing step's log and the run's inputs. Record the first error line.
4. If the failure is a cloud login, load `skills/pipelines-oidc-federation/SKILL.md`. Do not add a client secret or an access key.
5. If a GitHub Actions failure is an action pin, a permission, or an expression, load `skills/pipelines-github-actions-authoring/SKILL.md`. An Azure DevOps YAML defect stays in `skills/pipelines-azure-devops-yaml/SKILL.md`.
6. Change the cause. A re-run of the same revision is not the fix. Say what you changed and which log line it answers.

Do not widen `permissions` or the federated subject to get a job unstuck.
