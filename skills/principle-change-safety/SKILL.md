---
name: principle-change-safety
description: "Placeholder principle. Apply before any change to Azure or AWS infrastructure, Terraform state, or CI/CD pipelines: read the plan, know the blast radius, have a tested rollback, and change one thing at a time. Full content tracked in issue #1."
license: MIT
---

# Change safety (placeholder)

This is the template every jstack skill follows. The full version is built under issue #1.

- Read the `terraform plan` (or pipeline diff) and call out every destroy, replace and IAM/RBAC change.
- State what the change touches and what could break, across subscriptions, accounts and environments.
- Write the rollback before the change.
- Make one change at a time, promote through environments with approvals, and verify before the next.
