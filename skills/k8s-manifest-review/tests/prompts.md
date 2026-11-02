# Prompts for k8s-manifest-review

Example asks for `k8s-manifest-review`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I add or change a Deployment, StatefulSet, DaemonSet, Job or CronJob.

### Expected for ask 1

- Load `k8s-manifest-review` and follow that file through its own done-when.
- Step: Read the live objects before you change them. Run `kubectl get deploy,sts,ds,pdb,netpol,sa -n example`. Record replicas, images and any disruption budget. Follow `principle-observe-before-you-fix`.
- Check: The image reference contains `@sha256:<digest>`.
- Done when: The rendered workload matches the requests, probes, security context, budget and policy above.

## Ask 2

Pin the image by digest.

### Expected for ask 2

- Load `k8s-manifest-review` and follow that file through its own done-when.
- Step: Pin the image by digest. Follow `pipelines-artifacts-releases` and `k8s-dockerfile-hardening`. `latest` and a moving tag are not a release. `imagePullPolicy` does not turn a tag into a pin.
- Check: CPU and memory requests are set. The memory limit is set. A CPU limit is justified or absent.
- Done when: `kubectl diff` is empty after apply, or the GitOps sync is healthy.
