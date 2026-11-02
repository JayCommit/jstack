# Prompts for azure-key-vault

Example asks for `azure-key-vault`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I create a Key Vault or change its network or authorization mode.

### Expected for ask 1

- Load `azure-key-vault` and follow that file through its own done-when.
- Step: Create the vault with RBAC authorization, soft delete and purge protection. Soft delete cannot be turned off. Set retention at creation. Use 90 days for production. Do not pass `--enable-rbac-authorization false`. Do not add an access policy on a new vault.
- Check: The new vault uses RBAC. No access policy was added.
- Done when: The vault is RBAC, purge-protected, and private once the endpoint is proven.

## Ask 2

On an existing vault that still uses access policies, create the RBAC assignments first and prove the app still reads.

### Expected for ask 2

- Load `azure-key-vault` and follow that file through its own done-when.
- Step: On an existing vault that still uses access policies, create the RBAC assignments first and prove the app still reads. Then switch the vault to RBAC in a separate reviewed change. Switching first drops policy access and causes an outage.
- Check: Soft delete retention is set. Purge protection is on for production.
- Done when: Callers have a role on one object plane, scoped to the vault.
