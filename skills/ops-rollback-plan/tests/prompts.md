# Prompts for ops-rollback-plan

Example asks for `ops-rollback-plan`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

A Terraform apply, an app deploy, a database migration, a network change, or an IAM change can reach production.

### Expected for ask 1

- Load `ops-rollback-plan` and follow that file through its own done-when.
- Step: Name the change type. Write the first rollback command on the change. Rehearse that command on dev or test and keep the output. Follow `principle-rollback-first`. If the rehearsal fails, do not promote.
- Check: The change record names the type and the first command.
- Done when: The first rollback command is on the change, and it has succeeded off production.

## Ask 2

Terraform.

### Expected for ask 2

- Load `ops-rollback-plan` and follow that file through its own done-when.
- Step: Terraform. Roll back with the previous configuration and a plan that reverses this diff. Save that plan and apply that file. Follow `terraform-plan-review`. State stays in the remote backend. Follow `terraform-state-backends`. A resource rollback is a reverse plan. Restoring a state snapshot is a state recovery, and it follows that skill. It is not the default rollback. Re-applying does not bring back data a destroy deleted. For a data store, the rollback is a restore you have already practised, or you do not apply.
- Check: That command has been run on dev or test, and the output is kept.
- Done when: The notes say what the command cannot restore.
