#!/usr/bin/env bash
# Exercise scripts/sync: create, unchanged, dry-run and stale-file removal.
set -euo pipefail

root=$(cd "$(dirname "$0")/../.." && pwd)
sync="$root/scripts/sync"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

target="$tmp/repo"
mkdir -p "$target"

out=$("$sync" --all "$target")
grep -q 'create principle-change-safety' <<<"$out"
test -f "$target/.github/skills/principle-change-safety/SKILL.md"
diff -rq "$root/skills/principle-change-safety" "$target/.github/skills/principle-change-safety"

out=$("$sync" --all "$target")
grep -q 'unchanged principle-change-safety' <<<"$out"

mkdir -p "$target/.github/skills/other-skill"
printf 'keep\n' > "$target/.github/skills/other-skill/keep.txt"

stale="$target/.github/skills/principle-change-safety/stale.txt"
printf 'junk\n' > "$stale"
out=$("$sync" --dry-run --all "$target")
grep -q 'update principle-change-safety' <<<"$out"
test -f "$stale"
test -f "$target/.github/skills/other-skill/keep.txt"

out=$("$sync" --all "$target")
grep -q 'update principle-change-safety' <<<"$out"
test ! -f "$stale"
test -f "$target/.github/skills/principle-change-safety/SKILL.md"
test -f "$target/.github/skills/other-skill/keep.txt"

before=$(mktemp -d)
cp -a "$target/." "$before/"
out=$("$sync" --dry-run --all "$target")
grep -q 'unchanged principle-change-safety' <<<"$out"
diff -rq "$before" "$target"

rm -rf "$target/.agents"
out=$("$sync" --target-dir .agents/skills 'principle-*' "$target")
grep -q 'create principle-change-safety' <<<"$out"
test -f "$target/.agents/skills/principle-change-safety/SKILL.md"

if "$sync" --all "$tmp/missing-repo" >/dev/null 2>&1; then
  printf 'expected a missing target to fail\n' >&2
  exit 1
fi
if "$sync" "$target" >/dev/null 2>&1; then
  printf 'expected a missing skill list to fail\n' >&2
  exit 1
fi
if "$sync" no-such-skill "$target" >/dev/null 2>&1; then
  printf 'expected an unknown skill to fail\n' >&2
  exit 1
fi
