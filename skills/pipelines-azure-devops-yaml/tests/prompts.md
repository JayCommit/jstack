# Prompts for pipelines-azure-devops-yaml

Example asks for `pipelines-azure-devops-yaml`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

A run failed or hung and you are about to edit the YAML.

### Expected for ask 1

- Load `pipelines-azure-devops-yaml` and follow that file through its own done-when.
- Step: When a run has already failed or hung, open that run and read the step that exited non-zero before you edit the YAML. Follow `principle-observe-before-you-fix`. Record the run, the stage, the job and the commit. A rerun of the same revision is not the fix. GitHub Actions failures follow `pipelines-github-actions-debugging` instead of this file.
- Check: `timeoutInMinutes` is set on every job.
- Done when: A pull-request run uses the pinned template and the named pool.

## Ask 2

Declare `trigger` and `pr` for the branches this pipeline should build.

### Expected for ask 2

- Load `pipelines-azure-devops-yaml` and follow that file through its own done-when.
- Step: Declare `trigger` and `pr` for the branches this pipeline should build. In Azure Repos Git the `pr` key is ignored. Pull-request builds come from a build validation branch policy. A pull-request build is not a production deploy. Follow `principle-change-safety`.
- Check: Each deploy is a `deployment` job that names an `environment`.
- Done when: The production stage is a deployment job whose environment has the checks in `pipelines-environments-approvals`.
