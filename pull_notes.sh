#!/bin/bash

set -e

REPO=$(git rev-parse --show-toplevel)
TMPDIR=$(mktemp -d)

trap 'git -C "$REPO" worktree remove --force "$TMPDIR" >/dev/null 2>&1 || rm -rf "$TMPDIR"' EXIT

git -C "$REPO" fetch origin main
git -C "$REPO" fetch overleaf master
git -C "$REPO" worktree add --detach "$TMPDIR" origin/main

rm -rf "$TMPDIR/notes"
mkdir -p "$TMPDIR/notes"

git -C "$REPO" archive overleaf/master '*.tex' | tar -x -C "$TMPDIR/notes"

git -C "$TMPDIR" add -A notes

if git -C "$TMPDIR" diff --cached --quiet; then
    echo "No changes to commit."
else
    git -C "$TMPDIR" commit -m "sync notes from Overleaf"
    git -C "$TMPDIR" push origin HEAD:main
fi
