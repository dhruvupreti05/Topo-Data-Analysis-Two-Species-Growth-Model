#!/bin/bash

set -euo pipefail

REPO=$(git rev-parse --show-toplevel)
MAX_RETRIES=5

for attempt in $(seq 1 "$MAX_RETRIES"); do
    echo "Sync attempt $attempt..."

    TMPDIR=$(mktemp -d)

    cleanup() {
        git -C "$REPO" worktree remove --force "$TMPDIR" >/dev/null 2>&1 || rm -rf "$TMPDIR"
    }

    git -C "$REPO" fetch origin main
    git -C "$REPO" fetch overleaf master

    git -C "$REPO" worktree add --detach "$TMPDIR" origin/main >/dev/null

    rm -rf "$TMPDIR/notes"
    mkdir -p "$TMPDIR/notes"

    git -C "$REPO" archive overleaf/master '*.tex' | tar -x -C "$TMPDIR/notes"

    git -C "$TMPDIR" add -A notes

    if git -C "$TMPDIR" diff --cached --quiet; then
        echo "No notes changes to commit."
        cleanup
        exit 0
    fi

    git -C "$TMPDIR" commit -m "sync notes from Overleaf"

    if git -C "$TMPDIR" push origin HEAD:main; then
        echo "Successfully synced notes from Overleaf."
        cleanup
        exit 0
    fi

    echo "Push was rejected because GitHub changed. Retrying..."
    cleanup
done

echo "Failed to push after $MAX_RETRIES attempts."
exit 1
