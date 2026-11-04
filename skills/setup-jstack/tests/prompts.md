# Prompts for setup-jstack

Example asks for `setup-jstack`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I install jstack on a machine or into a repository.

### Expected for ask 1

- Load `setup-jstack` and follow that file through its own done-when.
- Step: Decide the tool and the scope. The scope is the whole pack, or a glob such as `terraform-*`, `azure-*`, `aws-*`, `pipelines-*`, `github-*`, `azuredevops-*`, `servicenow-*`, `k8s-*`, `gitops-*`, `policy-*`, `ops-*`, or `principle-*`. A repository that has no cluster does not need the Kubernetes skills. A repository that does not use ServiceNow does not need the ServiceNow skills. Write the choice down.
- Check: The tool and the skill glob are named before the copy.
- Done when: The chosen tool can see the skills in the scope you named.

## Ask 2

Cursor uses the plugin.

### Expected for ask 2

- Load `setup-jstack` and follow that file through its own done-when.
- Step: Cursor uses the plugin. The manifest is `.cursor-plugin/plugin.json`. It points `skills` at `./skills/` and `agents` at `./agents/`. Install the plugin from this repository. Do not also copy the same skills into the project.
- Check: Cursor is the plugin, or the sync, not both for the same skills.
- Done when: A second dry run reports `unchanged` for each of those skills.
