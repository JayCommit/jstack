# Prompts for terraform-drift

Example asks for `terraform-drift`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

A scheduled `terraform plan` reports changes nobody shipped in this commit.

### Expected for ask 1

- Load `terraform-drift` and follow that file through its own done-when.
- Step: Run the check on a schedule from the default branch. Use the plan identity, not the apply identity. See `principle-least-privilege`. Authenticate with OIDC or workload identity federation. See `principle-no-static-credentials`.
- Check: The scheduled job can plan and cannot apply. Its identity is federated and is not Owner or `AdministratorAccess`.
- Done when: The schedule records exit 0, or exit 2 has an owner and one chosen path.

## Ask 2

Plan with a lock and a detailed exit code.

### Expected for ask 2

- Load `terraform-drift` and follow that file through its own done-when.
- Step: Plan with a lock and a detailed exit code. Save the plan as an artifact. Do not apply it in this job. Pin the reviewed Terraform release, such as `1.10.5`.
- Check: Exit 1 is fixed as a failure. Exit 2 is a tracked review, not an automatic apply.
- Done when: That path is in git as a code change or an `import` block, or the live mistake was reverted.
