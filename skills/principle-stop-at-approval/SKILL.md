---
name: principle-stop-at-approval
description: "Use when an agent is about to apply, merge, deploy, or grant access for Azure, AWS, Terraform, or a pipeline. Prepare the diff and stop at the human approval that already exists."
license: MIT
---

# Stop at approval

The agent prepares the change. A person approves it. The pipeline applies it. Finishing faster is not a reason to skip the gate.

## Use when

- An agent is about to apply, merge, deploy, or grant access.
- The task would be quicker if the agent approved its own pull request.
- A missing permission tempts a standing grant so the agent can finish.
- A secret, a token, or a kubeconfig would have to be pasted into the chat.

## Rules

- Prepare the diff, the saved plan, the rollback, and the check. Then stop. A person approves in the pull request or the environment. The pipeline applies. Follow `pipelines-environments-approvals` and `pipelines-terraform-workflow`.
- A local `terraform plan` is a read. `terraform apply`, `az deployment`, `aws cloudformation deploy`, `helm upgrade`, and `kubectl` changes against a live cluster are not. Do not run those from the chat, including against dev.
- Do not merge, approve, or dismiss a required review on the change you just wrote.
- Do not grant a role, open a security group, or weaken an SCP so the task can proceed. A missing permission is a separate reviewed change. Follow `principle-least-privilege`.
- Do not put a secret, a token, a kubeconfig, or a cloud key in the chat, the pull request, or the command line. Follow `ops-secrets-handling`.
- If the repo does not name the subscription, the account, or the hostname, stop and ask. Do not invent one.

## Red flags

- The agent applies from a laptop or a chat and calls the pipeline optional.
- The agent approves, merges, or bypasses the gate on its own change.
- A temporary Owner or `AdministratorAccess` has no expiry, or it exists so the agent can finish.
- A secret value or a kubeconfig is in the transcript.

## Done when

- The change is a reviewed diff or a saved plan, waiting on the existing gate.
- Any wider access was refused here and written as its own change, or it was not needed.
- The chat and the pull request contain no secret value.
