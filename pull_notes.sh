#! /bin/bash

set -e

git fetch overleaf
git checkout main
git merge overleaf/master

mkdir -p notes

for file in *.tex; do
    [ -e "$file" ] || continue
    git mv "$file" notes/
done

git commit -m "retrieve .tex documents from overleaf"
git push origin main
