# Prompts for github-pull-requests

Example asks for `github-pull-requests`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I open a pull request, or you review one.

### Expected for ask 1

- Load `github-pull-requests` and follow that file through its own done-when.
- Step: Branch from the default branch. One change. Follow `principle-change-safety`. Do not commit secrets. Follow `ops-secrets-handling`.
- Check: The pull request targets the protected default branch.
- Done when: The pull request is open with the checks and the rollback written down, and it is waiting on a reviewer who is not the author.

## Ask 2

Open the pull request into the default branch.

### Expected for ask 2

- Load `github-pull-requests` and follow that file through its own done-when.
- Step: Open the pull request into the default branch. The body says what changed, how you checked it, and the rollback. If this can reach production, include the ServiceNow change number. Follow `servicenow-changes`. Do not invent that number.
- Check: The body names the check you ran and, for production, the ServiceNow change number.
- Done when: Or a person has merged it under the ruleset, the head branch is gone, and production has not moved without its approval.
