---
name: ops-certificates
description: "Use when a TLS certificate is expiring or you issue, renew, or bind one on Azure or AWS. Inventory every listener, renew into the store you already use, and prove the new certificate before you remove the old one."
license: MIT
---

# Certificates

Renew into the store you already have, bind it, and prove which certificate the client sees. Turning verification off is not a renewal.

## Use when

- A certificate expires inside the renewal window, or an alert fires for expiry.
- You issue, renew, or bind TLS on Application Gateway, Front Door, an ingress, an ALB, CloudFront, or API Management.
- Someone proposes to disable TLS verification, or to paste a private key into git or a pipeline variable.
- A hostname starts serving the wrong certificate after a bind.

## Steps

1. List the name, the issuer, the expiry, and every binding: listener, ingress, distribution, or custom domain. An expiry with no binding list is not a plan. Read the alert before you change the binding. Follow `principle-observe-before-you-fix`.

2. Renew into the home you already use. On Azure that is a Key Vault certificate. Follow `azure-key-vault`. On AWS that is ACM in the same region as the listener. A CloudFront certificate is requested in `us-east-1`. Do not paste the private key into git, a pipeline variable, or the chat. Follow `ops-secrets-handling`.

3. Bind the new certificate where the platform can hold it beside the old one, or in one change that keeps the old binding until the probe passes. One listener. Follow `principle-change-safety`. Do not set the listener to ignore certificate errors.

4. Prove the hostname still resolves and the new certificate is the one the client sees. Use the hostname the service already publishes. In examples that name is `example.com`. Do not invent a public name for the check.

   ```bash
   curl --verbose --show-error --fail-with-body --head "https://example.com"
   ```

5. A renewal does not change DNS. Change the record only when the name itself moves. Follow `azure-networking` or `aws-vpc`.

6. Remove the old binding after the probe is green. Keep the previous certificate until the rollback window you wrote down has passed. Deleting the only remaining copy is not a rollback.

7. Page before expiry, with enough time to renew and to roll back. That lead time is written on the alert. A page on the expiry day is late. Follow `ops-observability-alerts`.

8. The agent prepares the bind and stops for approval. Follow `principle-stop-at-approval`. Name the listeners and the pipeline. Follow `ops-blast-radius` when the certificate is on a shared gateway.

## Safety checks

- Every binding for this name is on the list.
- The new certificate is in Key Vault or ACM. The private key is not in git or the chat.
- A CloudFront certificate is in `us-east-1`. Any other listener uses the certificate in its own region.
- The probe shows the new certificate on the existing hostname.
- DNS was left as it is, unless the name itself moved.
- TLS verification was not disabled.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

Put the previous certificate back on the same listener. That bind is the rehearsed rollback. Follow `principle-rollback-first`. If the certificate object was deleted, recover it. Key Vault recovery is `azure-key-vault`. Do not mint a new self-signed certificate to get the site up. If the rollback bind fails, treat it as an incident. Follow `ops-incident-response`.

## Done when

- Clients on the existing hostname see the new certificate, and the probe output is kept.
- The old binding is gone, and the previous certificate still exists until the rollback window ends.
- The expiry alert fires before the day of expiry.
