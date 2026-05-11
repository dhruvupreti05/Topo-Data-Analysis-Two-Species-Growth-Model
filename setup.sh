#!/bin/bash
set -e

set -a
source .env
set +a

git remote add overleaf https://git.overleaf.com/$OVERLEAF_ID

if ! git remote | grep -q 'overleaf'; then
    git remote add overleaf "https://git.overleaf.com/$OVERLEAF_ID"
    echo "Added Overleaf remote."
else
    echo "Overleaf remote exists"
fi

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m ipykernel install --user --name=repo-env --display-name "Repository Environment"

echo ""
echo "Setup complete."
echo "Activate the environment with: `source .env/bin/activate`"
