#!/usr/bin/sh
script_dir="$(realpath "$0")"
base_dir="$(dirname "$(dirname "$script_dir")")"
pyenv_dir="$base_dir/.venv"

mkdir $pyenv_dir

# Create virtualenv
python3 -m venv "$pyenv_dir"

# Activate the virtual environment
source "$pyenv_dir/bin/activate"

cd $pyenv_dir
pip install --upgrade pip

# Install necessary packages for Jupyter
pip install ipykernel
pip install notebook
pip install pyedflib
python -m pip install git+https://github.com/GAA-UAM/scikit-fda.git@develop

# Add the virtual environment to Jupyter
python -m ipykernel install --user --name=venv --display-name "Python (venv)"