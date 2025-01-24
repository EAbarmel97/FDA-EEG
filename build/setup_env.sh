#!/usr/bin/sh
# Create virtualenv
python3 -m venv ./.venv

# Activate the virtual environment
source ./.venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install necessary packages for Jupyter
pip install ipykernel
pip install notebook
pip install -r requirements.txt

# Add the virtual environment to Jupyter
python -m ipykernel install --user --name=venv --display-name "Python (venv)"
