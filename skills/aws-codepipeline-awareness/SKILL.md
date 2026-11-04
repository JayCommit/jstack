---
name: aws-codepipeline-awareness
description: "Use when you read, change or replace a CodePipeline or CodeBuild project. Keep a working pipeline on its current tool, and start a new deploy on GitHub Actions with OIDC."
license: MIT
---

# CodePipeline and CodeBuild

Read the pipeline before you touch it. A pipeline that already deploys stays on that tool until a reviewed move. A new deploy uses GitHub Actions and OIDC.

## Use when

- You open a CodePipeline pipeline, a CodeBuild project or a CodeConnections connection.
- A build fails and someone wants to add a key, turn on privileged mode, or click a retry.
- You are deciding whether a new deploy belongs in CodePipeline or in GitHub Actions.
- You plan to move an existing pipeline to GitHub Actions.

## Steps

1. Read the pipeline and the projects before you change them. Run `aws codepipeline get-pipeline --name example` and `aws codebuild batch-get-projects --names example`. Record the pipeline type, the source action, each build project's environment and the service roles. Follow `principle-observe-before-you-fix`.

2. Keep a pipeline that already deploys. Fix it in place when the failure is in that pipeline. Move it only when the change record says why, and move it as its own change. Do not migrate the pipeline and change the application in the same release. Follow `principle-change-safety`.

3. Start a new deploy on GitHub Actions. The job uses `id-token: write` and the role from `aws-iam-least-privilege`. Follow `principle-no-static-credentials`. CodePipeline remains the right tool when the organization already requires the deploy to stay inside AWS, or when the pipeline you are editing is the one that ships today.

4. CodeCommit is a normal source when the repository is already there. Do not stand up a new CodeCommit repository for a codebase that already lives on GitHub. A GitHub source uses a CodeConnections connection. Do not store a personal access token in the pipeline, in CodeBuild, or in a parameter.

5. New CodePipeline pipelines use type V2. Leave an existing V1 pipeline on V1 until a reviewed change switches the type. A type change alters how executions queue. Turn polling off and let EventBridge start the pipeline.

6. CodeBuild's service role is the build's API calls, written as in `aws-iam-least-privilege`. `privilegedMode` is on only when the project builds a container image, and that project's role cannot administer the account. Do not set `AWS_ACCESS_KEY_ID` or `AWS_SECRET_ACCESS_KEY` in the project environment. Plain text environment variables are not a secret store. Follow `aws-secrets-ssm`.

7. A production stage has a manual approval. The approval is a person, not the same role that deploys. Artifacts sit in a bucket that blocks public access, encrypts with a key you name, and is not the state bucket.

8. On a failure, open the action log and the build phase that exited non-zero. Retry the same revision after you know the cause. A retry of a red build with a new access key hides the failure. Follow `principle-observe-before-you-fix`.

9. A move to GitHub Actions maps each stage to a job, keeps the same deploy role's permissions, and switches the trust to the OIDC subject. Follow `principle-rollback-first`: the old pipeline stays able to deploy until the new one has shipped once to a non-production account. Then remove the old pipeline in a later change.

10. If Terraform or CloudFormation owns the pipeline, plan that change on its own. Follow `terraform-plan-review` and `terraform-state-backends`. Name the account, the pipeline and the source repository.

## Safety checks

- You read the pipeline JSON and the project environment before editing.
- A new deploy is GitHub Actions with OIDC, or the change record says why it stays in CodePipeline.
- No personal access token and no static AWS key is stored on the project.
- `privilegedMode` is off, or it is an isolated image build whose role is not an admin role.
- Production has a manual approval. Artifacts are encrypted and not public.
- A migration does not also change the application, and the old pipeline still deploys until the new one has shipped once.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

Write the rollback before production. Follow `principle-rollback-first`.

1. Keep the previous pipeline definition from `get-pipeline`. Remove the `metadata` object before `update-pipeline`. Putting that pipeline object back is the rollback. Rehearse it on a non-production pipeline.
2. Leave the old pipeline disabled, not deleted, until the replacement has deployed once.
3. Stop if the only way forward is a static key or a privileged project with an admin role.

## Done when

- The pipeline that ships is the one you read, or the replacement has deployed once beside it.
- The build role, the source connection and the approval match this skill.
- No static credential was added to get a build green.
