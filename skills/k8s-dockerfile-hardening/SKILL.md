---
name: k8s-dockerfile-hardening
description: "Use when you write or review a Dockerfile. Build in stages, run as a non-root user, pin the base image by digest, and scan the image before anyone deploys it."
license: MIT
---

# Dockerfile hardening

The final image contains the app and nothing it does not need to run. The base is pinned. The process is not root.

## Use when

- You add or edit a Dockerfile or a container build.
- An image still uses a floating tag, runs as root, or ships a compiler in the final stage.
- A build argument or a copied file is carrying a secret into a layer.
- You are about to push an image that has not been scanned.

## Steps

1. Read the Dockerfile and the last image scan before you change the build. Record the base you run today and any finding you have not accepted. Follow `principle-observe-before-you-fix` when the build is already failing.

2. Build in stages. The builder stage may have a compiler and a package manager. The final stage copies the binary or the built app and does not copy the toolchain, the package lists, or the source. A one-stage image that starts from a full SDK is unfinished.

3. Pin every `FROM` by digest. A tag moves when the publisher rebuilds it. Put the tag you reviewed in a comment so a person can see it. The pin is the digest. Replace `<digest>` with the digest you pulled and reviewed. Do not use `latest`. `--link` and a secret mount need BuildKit. Add a `.dockerignore` that excludes `.git`, `.env` and `*.tfstate` before a `COPY` of the build context.

   ```dockerfile
   # bookworm, reviewed
   FROM example-base:bookworm@sha256:<digest> AS build
   WORKDIR /src
   COPY --link . .
   RUN make build

   # nonroot, reviewed
   FROM example-base:nonroot@sha256:<digest>
   COPY --from=build --chown=65532:65532 /src/bin/app /app
   USER 65532:65532
   ENTRYPOINT ["/app"]
   ```

4. Use a minimal final base. A static binary can use an empty base. Anything else uses a non-root base you have scanned, not the SDK image from the builder. When you set a syntax directive, pin that frontend image by digest as well.

5. Run as a numeric user. `USER 65532:65532` matches the non-root base above. Do not add a password or a sudoers entry. Do not switch to root in an entrypoint script. This skill is for Linux images. A Windows image is its own design.

6. Keep secrets out of layers. Pass a build secret with a BuildKit mount. Do not put a token in `ARG` or `ENV`. Do not `COPY` a `.env`, a key file, or a Terraform state.

   ```dockerfile
   RUN --mount=type=secret,id=example,dst=/run/secrets/example ./fetch.sh
   ```

7. If you must install packages, pin the package versions, then delete the package lists in the same `RUN`. A suppression of a pin rule names the rule and the reason. Do not pipe a remote script into a shell.

8. The image must still start when the root filesystem is read-only. Write only to a path the manifest mounts. The probe and the security context live on the workload. Follow `k8s-manifest-review`. Do not add a Docker `HEALTHCHECK` that repeats the Kubernetes probe.

9. Lint the Dockerfile with Hadolint. Scan the built image before the push. A finding you accept names the CVE, the reason and an expiry. The push, the digest deploy, the SBOM and the attestation are `pipelines-artifacts-releases`. This scan is the gate in front of that push. The scan step exits non-zero, and the push step is after it.

   ```text
   hadolint Dockerfile
   trivy image --severity HIGH,CRITICAL --exit-code 1 --ignore-unfixed example.com/example-repo@sha256:<digest>
   ```

10. Give the scan job no registry write. The push job is federated and can push only this repository. Follow `pipelines-github-actions-authoring` and `pipelines-oidc-federation`. One image change. Name the registry and the pipeline. Follow `principle-change-safety`. A larger base and a registry full of untagged digests are a cost. Follow `principle-cost-awareness`.

## Safety checks

- The final stage has no compiler and no package manager cache.
- Every `FROM` is pinned with `@sha256:<digest>`. No stage uses `latest`.
- The process user is a numeric non-root user, and the entrypoint does not switch back to root.
- No secret is in `ARG`, `ENV`, a copied file, or a layer history.
- Hadolint and `trivy image` both fail the job on a new finding.
- An accepted CVE has an id, a reason and an expiry.
- The push runs only after the scan exits 0, and it follows `pipelines-artifacts-releases`.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

Deploy the previous digest. Follow `pipelines-artifacts-releases` and `principle-rollback-first`. Do not rebuild an old tag and call that a rollback. Leave the previous digest in the registry until the rollback has been tried. A bad digest stays. You ship a new digest rather than overwriting a tag.

## Done when

- The Dockerfile matches the staged, non-root, digest-pinned shape above.
- Hadolint and the image scan are green, or every remaining finding is accepted with an expiry.
- The registry has the new digest, and no environment is deploying a moving tag.
- The change is verified with that digest in a non-production environment before anyone promotes it.
