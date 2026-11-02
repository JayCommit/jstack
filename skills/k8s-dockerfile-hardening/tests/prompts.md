# Prompts for k8s-dockerfile-hardening

Example asks for `k8s-dockerfile-hardening`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I add or edit a Dockerfile or a container build.

### Expected for ask 1

- Load `k8s-dockerfile-hardening` and follow that file through its own done-when.
- Step: Read the Dockerfile and the last image scan before you change the build. Record the base you run today and any finding you have not accepted. Follow `principle-observe-before-you-fix` when the build is already failing.
- Check: The final stage has no compiler and no package manager cache.
- Done when: The Dockerfile matches the staged, non-root, digest-pinned shape above.

## Ask 2

Build in stages.

### Expected for ask 2

- Load `k8s-dockerfile-hardening` and follow that file through its own done-when.
- Step: Build in stages. The builder stage may have a compiler and a package manager. The final stage copies the binary or the built app and does not copy the toolchain, the package lists, or the source. A one-stage image that starts from a full SDK is unfinished.
- Check: Every `FROM` is pinned with `@sha256:<digest>`. No stage uses `latest`.
- Done when: Hadolint and the image scan are green, or every remaining finding is accepted with an expiry.
