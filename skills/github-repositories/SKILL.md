---
name: github-repositories
description: "Use when you create or protect a GitHub repository. Keep it private unless the change says otherwise, protect the default branch with a ruleset, and turn on secret scanning where the plan allows."
license: MIT
---

# GitHub repositories

A repository ships through a pull request. The default branch is protected. Workflow files inside it follow `pipelines-github-actions-authoring`. This skill is the repository itself.

## Use when

- You create a repository, or you change who can push, merge, or delete it.
- The default branch has no ruleset, no CODEOWNERS, or an admin bypass.
- You turn on secret scanning, push protection, or Dependabot alerts.
- A public repository would run a self-hosted runner. Follow `pipelines-runners`.

## Steps

1. Name the organisation and the repository. Private is the default. Public is a written decision. Do not invent an organisation. The agent prepares the settings and stops before anyone bypasses a ruleset. Follow `principle-stop-at-approval`.

2. Create the repository in that organisation. Leave the wiki off unless the change asks for it. Do not put a secret in the first commit. Follow `ops-secrets-handling`.

   ```bash
   gh repo create example-org/example --private --disable-wiki
   ```

3. Use the default branch name the organisation already uses. Protect that branch with one repository ruleset, unless an organisation ruleset already covers this repository. Do not add a second ruleset that contradicts the first. Block deletion and force-push. Require a pull request, code-owner review, and the status checks the organisation already names. Leave the bypass list empty unless the change names a break-glass actor. Follow `ops-access-review` for that actor.

4. Put CODEOWNERS at `.github/CODEOWNERS` for the paths this repository ships, then require code-owner review. A ruleset that requires code owners, with an empty CODEOWNERS file, names nobody.

5. Turn on secret scanning and push protection where the plan allows. Enable Dependabot alerts. If the plan cannot store a control, write that on the change. Do not claim the control is on.

   ```bash
   gh repo edit example-org/example --enable-secret-scanning
   gh repo edit example-org/example --enable-secret-scanning-push-protection
   gh api --method PUT repos/example-org/example/vulnerability-alerts
   ```

6. Delete head branches after merge. Keep the merge method the organisation already uses. Workflow permissions in this repository start at read. The workflow contents follow `pipelines-github-actions-authoring`. Do not grant a repository-wide write so one workflow can pass.

7. A pull request into this repository follows `github-pull-requests`. A change that can reach production also has a ServiceNow change. Follow `servicenow-changes`.

## Safety checks

- The organisation and the visibility are the ones named on the change.
- The default branch cannot be deleted or force-pushed, and it requires a pull request.
- CODEOWNERS covers the paths this repository ships.
- The ruleset bypass list is empty, or the change names the break-glass actor.
- Secret scanning and Dependabot are on, or the plan gap is written down.
- No secret is in the repository or the chat.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

Delete a repository only when it has never held shared history. Otherwise revert the ruleset and CODEOWNERS to the previous settings in a pull request. Follow `principle-rollback-first`. Turning protection off is not a rollback. Follow `github-pull-requests` to land the revert.

## Done when

- The repository is private, or the change records why it is public.
- The default branch is covered by one ruleset and a CODEOWNERS file.
- Secret scanning, push protection, and Dependabot alerts are on, or the plan cannot store them and the change says so.
