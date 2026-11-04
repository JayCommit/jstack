# Prompts for github-repositories

Example asks for `github-repositories`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I create a repository, or you change who can push, merge, or delete it.

### Expected for ask 1

- Load `github-repositories` and follow that file through its own done-when.
- Step: Name the organisation and the repository. Private is the default. Public is a written decision. Do not invent an organisation. The agent prepares the settings and stops before anyone bypasses a ruleset. Follow `principle-stop-at-approval`.
- Check: The organisation and the visibility are the ones named on the change.
- Done when: The repository is private, or the change records why it is public.

## Ask 2

Create the repository in that organisation.

### Expected for ask 2

- Load `github-repositories` and follow that file through its own done-when.
- Step: Create the repository in that organisation. Leave the wiki off unless the change asks for it. Do not put a secret in the first commit. Follow `ops-secrets-handling`.
- Check: The default branch cannot be deleted or force-pushed, and it requires a pull request.
- Done when: The default branch is covered by one ruleset and a CODEOWNERS file.
