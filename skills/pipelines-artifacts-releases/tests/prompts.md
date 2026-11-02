# Prompts for pipelines-artifacts-releases

Example asks for `pipelines-artifacts-releases`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I publish a container image to Amazon ECR, Azure Container Registry or GitHub Container Registry.

### Expected for ask 1

- Load `pipelines-artifacts-releases` and follow that file through its own done-when.
- Step: Build and push in one job, and publish the digest as a job output. Later jobs deploy `<registry>/example-repo@sha256:<digest>`. They do not run the build again. Follow `principle-change-safety` and `pipelines-environments-approvals`.
- Check: One build produces the digest that development, test and production run.
- Done when: The registry shows one digest for this release, with the git SHA tag and the version tag pointing at it.

## Ask 2

Log in with federation.

### Expected for ask 2

- Load `pipelines-artifacts-releases` and follow that file through its own done-when.
- Step: Log in with federation. Follow `pipelines-oidc-federation`. The push role can push to this repository and cannot change IAM. Follow `aws-iam-least-privilege` and `principle-least-privilege`. For Azure in `uksouth`, use `azure/login` and then the registry login. Do not store a registry password.
- Check: The deploy reference contains `@sha256:<digest>`. It is not a moving tag.
- Done when: Each environment runs that digest, and `gh attestation verify` succeeded, or the plan gap is written down.
