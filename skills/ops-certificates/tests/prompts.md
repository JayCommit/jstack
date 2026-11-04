# Prompts for ops-certificates

Example asks for `ops-certificates`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

A certificate expires inside the renewal window, or an alert fires for expiry.

### Expected for ask 1

- Load `ops-certificates` and follow that file through its own done-when.
- Step: List the name, the issuer, the expiry, and every binding: listener, ingress, distribution, or custom domain. An expiry with no binding list is not a plan. Read the alert before you change the binding. Follow `principle-observe-before-you-fix`.
- Check: Every binding for this name is on the list.
- Done when: Clients on the existing hostname see the new certificate, and the probe output is kept.

## Ask 2

Renew into the home you already use.

### Expected for ask 2

- Load `ops-certificates` and follow that file through its own done-when.
- Step: Renew into the home you already use. On Azure that is a Key Vault certificate. Follow `azure-key-vault`. On AWS that is ACM in the same region as the listener. A CloudFront certificate is requested in `us-east-1`. Do not paste the private key into git, a pipeline variable, or the chat. Follow `ops-secrets-handling`.
- Check: The new certificate is in Key Vault or ACM. The private key is not in git or the chat.
- Done when: The old binding is gone, and the previous certificate still exists until the rollback window ends.
