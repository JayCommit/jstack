# Prompts for principle-idempotent-automation

Example asks for `principle-idempotent-automation`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I write or change Terraform, a shell or PowerShell script, a GitHub Actions workflow or an Azure DevOps pipeline.

### Expected for ask 1

- Load `principle-idempotent-automation` and follow that file through its own done-when.
- Rule: Apply the saved plan, then plan again with no further edits. The second `terraform plan -detailed-exitcode` should exit 0. If it still reports changes, the configuration is not stable. How the plan was saved is in `principle-change-safety`.
- Red flag: The second run fails because the resource already exists.
- Done when: A second run with the same inputs exits successfully and changes nothing.

## Ask 2

Scripts create or update.

### Expected for ask 2

- Load `principle-idempotent-automation` and follow that file through its own done-when.
- Rule: Scripts create or update. A create call that fails when the resource already exists is unfinished. In Bash, start with `set -euo pipefail` and test the condition you branch on.
- Red flag: Two production applies can run at the same time against one state file.
- Done when: Production applies for one state or environment are serialised.
