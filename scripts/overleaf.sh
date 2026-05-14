#!/bin/bash

# Script pulls LaTeX files from Overleaf, compiles with pdfLatex, pushes .tex files, respective .pdf's and figures to remote under notes/

set -e

REPO=$(git rev-parse --show-toplevel)
TMPDIR=$(mktemp -d)

cd "$REPO"

trap 'rm -rf "$TMPDIR"; git -C "$REPO" worktree prune >/dev/null 2>&1' EXIT

git -C "$REPO" fetch origin main
git -C "$REPO" fetch overleaf master
git -C "$REPO" worktree add --detach "$TMPDIR" origin/main

rm -rf "$TMPDIR/notes"
mkdir -p "$TMPDIR/notes/pdfs"

git -C "$REPO" archive overleaf/master | tar -x -C "$TMPDIR/notes"

cd "$TMPDIR/notes"

for file in *.tex; do
    [ -e "$file" ] || continue

    if grep -Fxq '% git ignore this file' "$file"; then
        echo "Ignoring $file"
        rm -f "$file"
        continue
    fi

    if grep -q '\\documentclass' "$file"; then
        pdflatex -interaction=nonstopmode -halt-on-error "$file"
        mv "${file%.tex}.pdf" pdfs/
    else
        echo "Skipping $file"
    fi
done

cd "$TMPDIR"

git add -A notes

if git diff --cached --quiet; then
    echo "No changes to commit."
else
    git commit -m "sync notes and PDFs from Overleaf"
    git push origin HEAD:main
fi
