# Remove

Remove only the jstack copy. Leave skills that came from somewhere else.

## A machine install

`gh skill` has no uninstall command. List the install, then delete the directory it prints.

```bash
gh skill list --scope user --agent github-copilot --json skillName,path,sourceURL
```

Delete a path only when `sourceURL` is this repository. Repeat with `--agent cursor`, `--agent claude-code`, or the agent you installed for. Add `--scope project` when the copy is inside a repository rather than your home directory.

## A repository copy

Delete the skill folders `scripts/sync` created under `.github/skills`, `.agents/skills`, or `.claude/skills`. A bad glob is fixed by deleting that directory and syncing the glob you meant.

If you copied personas, prompts, or path rules by hand, delete those copies of `agents/`, `.github/prompts/`, and `.github/instructions/`. The sync script does not own them.

## Cursor's plugin

Remove the jstack plugin from Cursor's plugin list. If you also copied skills into the project, delete that copy too. One install path is enough.

The copy does not change Azure or AWS. Deleting it does not roll back a cloud resource.
