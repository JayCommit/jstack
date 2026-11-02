# Prompts for terraform-workspaces-environments

Example asks for `terraform-workspaces-environments`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I lay out dev, test and prod for Azure or AWS.

### Expected for ask 1

- Load `terraform-workspaces-environments` and follow that file through its own done-when.
- Step: Prefer one directory per environment. Apply from that directory so the state key is obvious. Do not also use workspaces inside those directories. Two mechanisms hide which state you wrote.
- Check: Each environment has its own state key, and the key is named on the pull request.
- Done when: Dev, test and prod each have a distinct backend key, or a workspace is used and its name was printed before apply.

## Ask 2

Give each directory its own backend key.

### Expected for ask 2

- Load `terraform-workspaces-environments` and follow that file through its own done-when.
- Step: Give each directory its own backend key. Keep the storage account or bucket in shared partial config. Keep the key in the environment file. Dev, test and prod must not share a key.
- Check: The directory, or the printed workspace, matches the environment you apply.
- Done when: The change promotes one pinned module version, not a copy of state.
