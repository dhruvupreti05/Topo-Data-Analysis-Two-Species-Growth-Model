#!/bin/bash

"""
This bash script sets up virtual environment as .venv, adds Overleaf project
as a remote Git repository, installs relevant libraries from requirements.txt 
and adds virtual environment to the Python Kernal of Jupyter Notebook.
"""

set -e

REPO=$(git rev-parse --show-toplevel)
cd "$REPO"

set -a
source .env
set +a

if ! git remote | grep -q 'overleaf'; then
    git remote add overleaf "https://git@git.overleaf.com/$OVERLEAF_ID"
    echo "Added Overleaf remote."
else
    echo "Overleaf remote exists"
fi

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r ./scripts/requirements.txt
python -m ipykernel install --user --name=repo-env --display-name "Repository Environment"

echo ""
echo "Setup complete."
echo "Activate the environment with: source .env/bin/activate"
