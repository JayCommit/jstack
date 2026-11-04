# Blinded review fixture

This directory is a review target. It is not a pattern to copy. The secure stack is `examples/jstack-sample`.

A trial reads `prompts.md` and the two files that page names. Leave `expected.md` closed until the review is written down. The values in the workflow are placeholders. Do not replace them with a real credential. `.gitleaks.toml` allowlists this directory because the workflow is planted.

Nothing here is applied. GitHub Actions runs only the workflows in the repository root, so `.github/workflows/deploy.yml` in this directory is not a live deploy.
