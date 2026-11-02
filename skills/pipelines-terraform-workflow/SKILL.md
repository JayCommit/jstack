---
name: pipelines-terraform-workflow
description: "Use when a pipeline runs Terraform for Azure or AWS. Lint with no cloud credential, plan on the pull request and comment a summary, then apply the saved plan from the merge commit after the environment approves, one environment at a time."
license: MIT
---

# Terraform plan and apply workflow

Lint with no cloud login. Plan on the pull request with a read-only identity. After merge, plan once more and apply that saved file after the environment approves it.

## Use when

- A pull request changes Terraform, tfvars or `.terraform.lock.hcl` for Azure or AWS.
- You wire fmt, validate, lint and scan into the same workflow as plan and apply.
- Someone wants `terraform apply` from a fork, from a laptop, or from a fresh plan at deploy time.

## Steps

1. On the pull request, run fmt, validate, tflint, Checkov and Trivy with no cloud credential. Follow `terraform-static-analysis`. That job keeps `permissions: contents: read`, sets `timeout-minutes`, and does not set `id-token: write`.

2. Use two federated identities per environment. Follow `pipelines-oidc-federation`, `aws-iam-least-privilege` and `azure-rbac-entra`. The plan identity reads the cloud and the state. It trusts the `:pull_request` subject and the `:ref:refs/heads/main` subject. The apply identity can change the stack and trusts only `:environment:production`. A plan takes the state lock, so the plan identity also needs the lock permission. If you keep it strictly read-only, run pull-request plans with `-lock=false` and never apply one of them.

3. Init the remote backend for this environment. One backend key per environment. Follow `terraform-state-backends` and `terraform-workspaces-environments`. Keep the Terraform version and `.terraform.lock.hcl` the same in plan and apply.

4. Plan on the pull request and comment a summary. Skip the job for a fork. A fork gets no OIDC token. Do not use `pull_request_target` to run pull-request code. `pull-requests: write` sits on this job only. Post the `Plan:` line and a link to the run, not the raw plan. Values that are not marked sensitive appear in clear text.

   ```yaml
   on:
     pull_request:
       paths: ["infra/**"]
   permissions:
     contents: read
   concurrency:
     group: tf-plan-${{ github.event.pull_request.number }}
     cancel-in-progress: true
   jobs:
     plan:
       if: github.event.pull_request.head.repo.full_name == github.repository
       runs-on: ubuntu-latest
       timeout-minutes: 20
       permissions:
         contents: read
         id-token: write
         pull-requests: write
       defaults:
         run:
           working-directory: infra
       steps:
         - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
           with:
             persist-credentials: false
         - uses: hashicorp/setup-terraform@dfe3c3f87815947d99a8997f908cb6525fc44e9e # v4.0.1
           with:
             terraform_version: 1.10.5
             terraform_wrapper: false
         - uses: aws-actions/configure-aws-credentials@e1253824e5c10ff9df46874f81ed3ec929e19cfd # v6.3.0
           with:
             role-to-assume: arn:aws:iam::123456789012:role/example-plan
             aws-region: eu-west-2
         - run: terraform init -input=false -backend-config=envs/production.backend.hcl
         - run: terraform plan -input=false -lock-timeout=5m -out=tfplan
         - name: Comment summary
           env:
             GH_TOKEN: ${{ github.token }}
             PR: ${{ github.event.pull_request.number }}
             RUN_URL: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
           run: |
             summary=$(terraform show -no-color tfplan | grep -E '^(Plan:|No changes)')
             gh pr comment "$PR" --body "production: ${summary} ([run](${RUN_URL}))"
   ```

5. Review the plan in the run log before anyone merges. Follow `terraform-plan-review` and `principle-change-safety`. The comment is a pointer, not the review.

6. After merge, plan again on the main branch, save it, and apply that file after the environment approves. Put `concurrency` on the workflow with one group per environment and `cancel-in-progress: false`, so a second run waits. The plan file holds secrets in clear text. Keep `retention-days` at 1 and limit who can read the workflow's artefacts. On Azure, swap the AWS login for `azure/login` from `pipelines-oidc-federation`.

   ```yaml
   on:
     push:
       branches: [main]
       paths: ["infra/**"]
   permissions:
     contents: read
   concurrency:
     group: tf-production
     cancel-in-progress: false
   jobs:
     plan:
       runs-on: ubuntu-latest
       timeout-minutes: 20
       permissions:
         contents: read
         id-token: write
       defaults:
         run:
           working-directory: infra
       steps:
         - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
           with:
             persist-credentials: false
         - uses: hashicorp/setup-terraform@dfe3c3f87815947d99a8997f908cb6525fc44e9e # v4.0.1
           with:
             terraform_version: 1.10.5
         - uses: aws-actions/configure-aws-credentials@e1253824e5c10ff9df46874f81ed3ec929e19cfd # v6.3.0
           with:
             role-to-assume: arn:aws:iam::123456789012:role/example-plan
             aws-region: eu-west-2
         - run: terraform init -input=false -backend-config=envs/production.backend.hcl
         - run: terraform plan -input=false -lock-timeout=5m -out=tfplan
         - uses: actions/upload-artifact@cf430e030ddbb5b0abf93d22962f4752f3646cd9 # v7.0.2
           with:
             name: tfplan-production
             path: infra/tfplan
             retention-days: 1
     apply:
       needs: plan
       runs-on: ubuntu-latest
       timeout-minutes: 30
       environment: production
       permissions:
         contents: read
         id-token: write
       defaults:
         run:
           working-directory: infra
       steps:
         - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
           with:
             persist-credentials: false
         - uses: hashicorp/setup-terraform@dfe3c3f87815947d99a8997f908cb6525fc44e9e # v4.0.1
           with:
             terraform_version: 1.10.5
         - uses: aws-actions/configure-aws-credentials@e1253824e5c10ff9df46874f81ed3ec929e19cfd # v6.3.0
           with:
             role-to-assume: arn:aws:iam::123456789012:role/example-apply
             aws-region: eu-west-2
         - uses: actions/download-artifact@9000827ccba6bdab643e8b6fd33ac0654aef8333 # v8.0.2
           with:
             name: tfplan-production
             path: infra
         - run: terraform init -input=false -backend-config=envs/production.backend.hcl
         - run: terraform apply -input=false -lock-timeout=5m tfplan
   ```

7. Do not run `terraform plan` again in the apply job. If the state changed after the plan, Terraform refuses the stale file. Re-run the workflow for a fresh plan and a fresh approval. Gate production with the reviewers in `pipelines-environments-approvals`.

8. Promote one environment at a time. Development, test and production each have a job pair, a backend key and an environment, chained with `needs`. Do not apply two environments from one plan.

9. After the apply, run `terraform plan -detailed-exitcode`. Exit 0 means no changes and 2 means drift or a change that did not converge. Follow `terraform-drift`. Price a plan that adds spend. Follow `principle-cost-awareness`. On a private repository, GitHub-hosted minutes are billed beyond the plan quota, and artefact storage counts.

## Safety checks

- The lint job has no cloud credential and no `id-token: write`.
- Plan and apply use different identities. The plan identity cannot change resources.
- The apply job applies the artefact from this run and does not plan again.
- `pull-requests: write` is set only on the job that comments, and the comment holds no raw plan.
- The plan artefact keeps for one day and only people who may see the state can read it.
- Fork pull requests do not plan with cloud access. `pull_request_target` is not used to run pull-request code.
- Each environment has its own concurrency group with `cancel-in-progress: false`.

## Rollback

Write the reverse change before the production apply. Follow `principle-rollback-first`. The rollback is a revert pull request that goes through the same plan, review and approval. If an apply fails part way, the saved plan is spent. Read the error and the state, then plan again from the same commit and review it before you apply. Do not apply by hand from a laptop.

## Done when

- fmt, validate, tflint, Checkov and Trivy ran without a cloud credential.
- The pull request showed a plan summary, and the reviewed change merged.
- The applied file is the plan saved from the merge commit, applied after approval.
- A later `terraform plan -detailed-exitcode` exits 0, or the change is stopped with the revert ready.
