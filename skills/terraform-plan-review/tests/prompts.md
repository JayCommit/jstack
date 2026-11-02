# Prompts for terraform-plan-review

Example asks for `terraform-plan-review`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I are about to run `terraform apply` for Azure or AWS.

### Expected for ask 1

- Load `terraform-plan-review` and follow that file through its own done-when.
- Step: Authenticate with OIDC or workload identity federation. Do not export a static access key, a storage account key or a client secret. See `principle-no-static-credentials`.
- Check: The file passed to `terraform apply` is the file that was reviewed.
- Done when: Exit 0 is recorded, or exit 2 was reviewed and that saved plan was applied.

## Ask 2

Init the remote backend for this environment.

### Expected for ask 2

- Load `terraform-plan-review` and follow that file through its own done-when.
- Step: Init the remote backend for this environment. Locking must be on. A plan that cannot lock is not ready to review.
- Check: Destroys, replacements, grants, network edits, moves, imports and lockfile bumps are listed, or the plan has none.
- Done when: The blast radius is written on the change.
