# Prompts for pipelines-environments-approvals

Example asks for `pipelines-environments-approvals`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

A job deploys, applies Terraform, or otherwise changes a shared environment.

### Expected for ask 1

- Load `pipelines-environments-approvals` and follow that file through its own done-when.
- Step: Create one GitHub environment per stage you promote through, such as `development`, `test` and `production`. Follow `principle-change-safety`. Do not point every job at `production`.
- Check: Production has a required reviewer who is not the author. Prevent self-review is on where the plan allows it.
- Done when: The production job does not start until a second person approves it.

## Ask 2

On `production`, add required reviewers and turn on prevent self-review so the author cannot approve their own run.

### Expected for ask 2

- Load `pipelines-environments-approvals` and follow that file through its own done-when.
- Step: On `production`, add required reviewers and turn on prevent self-review so the author cannot approve their own run. Add a wait timer when the release needs a pause before the job starts. Limit deployment branches and tags to the branch or tag you actually ship. Turn off the setting that lets administrators bypass the rules, unless the change record says who may bypass and why. Keep secrets the deploy needs as environment secrets on `production`, not repository secrets. On a private repository, some protection rules are not available on every plan. Check your plan. Do not claim a rule is active when the UI cannot store it.
- Check: Deployment branches and tags, or an Azure DevOps branch control check, name the ref that may deploy.
- Done when: The federated subject matches that environment and no wider ref.
