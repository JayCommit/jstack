---
description: "Review a Terraform plan or module diff before anyone applies it. List destroys, grants, network edits, and provider bumps."
---

# Plan review

Load `skills/terraform-plan-review/SKILL.md` and `skills/principle-change-safety/SKILL.md`. When the plan can reach production, also load `skills/principle-rollback-first/SKILL.md`.

Read the whole plan. List every destroy, replace, IAM or RBAC grant, network edit, move, import, and provider or module bump. Say whether the plan was saved. Name the subscription or account, the state key, and the pipeline. Do not apply.
