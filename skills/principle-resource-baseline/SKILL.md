---
name: principle-resource-baseline
description: "Use when you create an Azure or AWS resource. Take the name from the scheme you already use, set the tags that account requires, and deny delete on state and vaults."
license: MIT
---

# Resource baseline

A new resource uses the names, tags, and delete protection the estate already uses. A second pattern for one resource is drift.

## Use when

- You create an Azure or AWS resource, a state backend, or a log sink.
- A resource has no environment tag, no owner, or a name you invented for this change.
- You are about to delete a state account, a key vault, or a backup vault.

## Rules

- Take the name from the scheme the repository already uses. If the repository has no scheme, write one short pattern and use it for every resource in the change. Do not invent a second prefix for a single resource.
- Use the tag keys the subscription or account already requires. When nothing is required yet, set `environment`, `owner`, `cost-centre` (or the existing `cost-center` key), and `data-class`. Do not add a second key for the same fact. Values are codes such as `prod` or `internal`. A person's name, an email, or a secret is not a tag value.
- Deny delete on the state backend, the key vault, and the backup vault. On Azure that is a CanNotDelete lock. On AWS that is a policy that denies delete of the bucket or the vault. This is not the Terraform state lock. Versioning and the state lock stay in `terraform-state-backends`. A delete lock is not a backup. Follow `ops-backup-restore` when the resource holds data.
- Send logs to the workspace, trail, or account the landing zone already has. Do not create a new Log Analytics workspace or a new CloudTrail trail per application. Flow logs follow `aws-vpc`. Retention and caps follow `principle-cost-awareness`.
- One resource, one owner in code. Follow `principle-everything-as-code`.

## Red flags

- A new name pattern appears for one resource while the rest of the subscription uses another.
- A production resource ships with no environment tag, or a tag value holds an email or a secret.
- The state account, key vault, or backup vault can be deleted by the pipeline that writes to it.
- The change creates a second log archive for one application.

## Done when

- The name matches the scheme already in the repository, or the change writes the one pattern it will keep using.
- The required tags are on the resource, and no tag value is a secret or a person's name.
- State, key vaults, and backup vaults deny delete, and logs go to the archive that already exists.
