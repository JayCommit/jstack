---
name: pipelines-artifacts-releases
description: "Use when you build an image or a package and promote it. Build once, deploy the digest, attach provenance and an SBOM, and keep registry tags immutable."
license: MIT
---

# Artefacts and releases

Build the image once. Every later environment deploys that digest. A tag is a name for the digest, not a thing you rebuild.

## Use when

- You publish a container image to Amazon ECR, Azure Container Registry or GitHub Container Registry.
- A release should move from development to test to production without a second build.
- You add build provenance, an SBOM, or a check that the digest was signed.
- A pipeline retags `latest` and deploys that tag.

## Steps

1. Build and push in one job, and publish the digest as a job output. Later jobs deploy `<registry>/example-repo@sha256:<digest>`. They do not run the build again. Follow `principle-change-safety` and `pipelines-environments-approvals`.

2. Log in with federation. Follow `pipelines-oidc-federation`. The push role can push to this repository and cannot change IAM. Follow `aws-iam-least-privilege` and `principle-least-privilege`. For Azure in `uksouth`, use `azure/login` and then the registry login. Do not store a registry password.

3. Pin every action. Set `timeout-minutes`. Workflow permissions stay `contents: read`. This job adds `id-token: write` and `attestations: write`, and repeats `contents: read`. Add `packages: write` only when the push target is GitHub Container Registry. On a private repository, GitHub-hosted minutes are billed beyond the plan quota. Larger runners are always billed. Artefact storage and cache storage count. Follow `principle-cost-awareness`.

   ```yaml
   on:
     push:
       tags: ["v*"]
   permissions:
     contents: read
   jobs:
     build:
       runs-on: ubuntu-latest
       timeout-minutes: 30
       outputs:
         digest: ${{ steps.build.outputs.digest }}
       permissions:
         id-token: write
         contents: read
         attestations: write
       steps:
         - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
           with:
             persist-credentials: false
         - uses: aws-actions/configure-aws-credentials@e1253824e5c10ff9df46874f81ed3ec929e19cfd # v6.3.0
           with:
             role-to-assume: arn:aws:iam::123456789012:role/example-push
             aws-region: eu-west-2
         - id: ecr
           uses: aws-actions/amazon-ecr-login@03f1aad4c6c7ffd436567f42f9384779290529bd # v2.1.7
         - uses: docker/setup-buildx-action@f87e5991a6d7451dcb8d9637bfbc97413f497069 # v4.4.1
         - id: build
           uses: docker/build-push-action@c3c9e263c25d99ce0380d002d59b67737d91b0dc # v7.4.0
           with:
             context: .
             push: true
             tags: |
               ${{ steps.ecr.outputs.registry }}/example-repo:${{ github.sha }}
               ${{ steps.ecr.outputs.registry }}/example-repo:${{ github.ref_name }}
         - uses: anchore/sbom-action@66cbf4bc1f1c0d2edc94016e65bc221b6bb0ad6c # v0.24.3
           with:
             image: ${{ steps.ecr.outputs.registry }}/example-repo@${{ steps.build.outputs.digest }}
             format: spdx-json
             artifact-name: sbom-example-repo.spdx.json
         - uses: actions/attest-build-provenance@4d101475d8b20a2381f78447822ac1eab6504dd8 # v4.2.2
           with:
             subject-name: ${{ steps.ecr.outputs.registry }}/example-repo
             subject-digest: ${{ steps.build.outputs.digest }}
             push-to-registry: true
   ```

4. The release tag, such as `v1.2.0`, and the git SHA tag both point at the one digest at build time. Do not move either tag later. Do not deploy `latest`. Turn on tag immutability in ECR. On ACR, lock tags or disable write so a tag cannot be replaced. Deploy the digest. Follow `pipelines-github-actions-authoring` for the pin and the concurrency on the deploy job, with `cancel-in-progress: false`.

5. For GitHub Container Registry, log in with `docker/login-action@81c6f93d4bc991e510b342a00b419b3bb4efc5c6 # v4.7.0` and the job token. Add `packages: write` on that job only. Do not put a registry password in the workflow.

6. Verify provenance before you deploy. Attestations on a private repository require GitHub Enterprise Cloud. Check your plan. If the plan cannot store attestations, say so on the change, keep the SBOM, and still deploy by digest.

   ```bash
   gh attestation verify oci://123456789012.dkr.ecr.eu-west-2.amazonaws.com/example-repo@sha256:<digest> --repo example-org/example-repo
   ```

7. Set `retention-days` on artefacts this workflow uploads with `actions/upload-artifact@cf430e030ddbb5b0abf93d22962f4752f3646cd9 # v7.0.2`. Keep the window short. Keep the SBOM you must retain with the release or in the registry beside the image. The image itself stays in the registry, not in a workflow artefact.

8. Record the digest on the release. Each environment deploys `needs.build.outputs.digest`, so a re-run deploys the same image. Follow `principle-idempotent-automation`.

## Safety checks

- One build produces the digest that development, test and production run.
- The deploy reference contains `@sha256:<digest>`. It is not a moving tag.
- ECR tag immutability is on, or ACR tags are locked or not writable.
- The build job sets `id-token: write`, `attestations: write` and `contents: read`.
- `packages: write` is present only on a job that pushes to GitHub Container Registry.
- Provenance was verified, or the plan cannot store attestations and the change says so.
- No registry password or cloud key is stored in the workflow.

## Rollback

Deploy the previous digest. Do not rebuild an old tag from a branch and call that a rollback. Follow `principle-rollback-first`. Leave the previous digest in the registry until the rollback has been tried. A bad tag is left immutable. You ship a new digest rather than overwriting it.

## Done when

- The registry shows one digest for this release, with the git SHA tag and the version tag pointing at it.
- Each environment runs that digest, and `gh attestation verify` succeeded, or the plan gap is written down.
- The SBOM is kept with the release, and the previous digest is still available to deploy.
