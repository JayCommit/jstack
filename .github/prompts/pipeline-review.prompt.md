---
description: "Review a GitHub Actions or Azure DevOps pipeline change. Check pins, permissions, timeouts, and how the job logs in to the cloud."
---

# Pipeline review

For a GitHub Actions workflow, load `skills/pipelines-github-actions-authoring/SKILL.md`. For an Azure DevOps pipeline, load `skills/pipelines-azure-devops-yaml/SKILL.md`. A job that calls Azure or AWS also loads `skills/pipelines-oidc-federation/SKILL.md`.

Read the diff. Check least-privilege permissions, full SHA pins or a protected template tag, a timeout on every job, and concurrency where deploys must not overlap. A cloud login uses federation. Do not add a client secret or an access key. Do not apply a workflow change by widening the token.
