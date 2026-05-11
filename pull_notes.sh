#!/bin/bash

set -e

REPO=$(git rev-parse --show-toplevel)
TMPDIR=$(mktemp -d)

trap 'rm -rf "$TMPDIR"; git -C "$REPO" worktree prune >/dev/null 2>&1' EXIT

git -C "$REPO" fetch origin main
git -C "$REPO" fetch overleaf master
git -C "$REPO" worktree add --detach "$TMPDIR" origin/main

mkdir -p "$TMPDIR/notes/pdfs"

git -C "$REPO" archive overleaf/master '*.tex' | tar -x -C "$TMPDIR/notes"

cd "$TMPDIR/notes"

for file in *.tex; do
    [ -e "$file" ] || continue
    [[ "$file" == _* ]] && continue

    pdflatex -interaction=nonstopmode -halt-on-error "$file"
    mv "${file%.tex}.pdf" pdfs/
done

cd "$TMPDIR"

git add -A notes

if ! git diff --cached --quiet; then
    git commit -m "sync notes and PDFs from Overleaf"
    git push origin HEAD:main
else
    echo "No changes to commit."
fi
