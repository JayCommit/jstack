# Prompts for ops-blast-radius

Example asks for `ops-blast-radius`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I plan or apply Terraform, or you edit a pipeline that deploys it.

### Expected for ask 1

- Load `ops-blast-radius` and follow that file through its own done-when.
- Step: Start from the object you mean to change. List what shares it. Write the list on the pull request. "Small" is not a list. Follow `principle-change-safety`.
- Check: The pull request names the subscription or account, the region, the network, the state key or cluster, and the pipeline.
- Done when: The pull request has the list from the safety checks, including how you looked for neighbours.

## Ask 2

Terraform.

### Expected for ask 2

- Load `ops-blast-radius` and follow that file through its own done-when.
- Step: Terraform. Read the backend key from the root module. Follow `terraform-state-backends`. Every person and every pipeline that uses that key is in the radius. `terraform state list` shows the addresses in this state. A module used by more than one root is more than one apply. Follow `terraform-workspaces-environments`.
- Check: Shared dependents are listed, or you wrote how you checked that there are none.
- Done when: The plan or the diff stays inside that list.
