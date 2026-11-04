# Prompts for azuredevops-repositories

Example asks for `azuredevops-repositories`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I create a repository, or you change branch policy or repository permissions.

### Expected for ask 1

- Load `azuredevops-repositories` and follow that file through its own done-when.
- Step: Use the organisation and project the user named, such as `https://dev.azure.com/example` and project `example`. Do not invent them. The agent prepares the policy and the pull request, then stops. Follow `principle-stop-at-approval`.
- Check: The repository is Git, in the named organisation and project.
- Done when: The default branch policy matches the checks above, or an existing organisation standard is the one you kept.

## Ask 2

Create a Git repository.

### Expected for ask 2

- Load `azuredevops-repositories` and follow that file through its own done-when.
- Step: Create a Git repository. Do not create a TFVC repository.
- Check: The default branch requires a reviewer who is not the author, and votes reset on a new push.
- Done when: The pull request is open and waiting on a reviewer, or a person has completed it with policy intact.
