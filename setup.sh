#!/bin/bash
set -e

python3 -m venv .venv
source ocean/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m ipykernel install --user --name=repo-env --display-name "Repository Environment"

echo ""
echo "Setup complete."
echo "Activate the environment with:"
echo "source ocean/bin/activate"
