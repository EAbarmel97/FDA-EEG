#!/usr/bin/sh
script_dir="$(realpath "$0")"
base_dir="$(dirname "$(dirname "$script_dir")")"
pyenv_dir="$base_dir/.venv"

mkdir $pyenv_dir

# create virtualenv
python3 -m venv "$pyenv_dir"

# activate the virtual environment
source "$pyenv_dir/bin/activate"

cd $pyenv_dir
pip install --upgrade pip

# install dependencies to use inside the venv
pip install pyedflib
python -m pip install git+https://github.com/GAA-UAM/scikit-fda.git@develop

#if current branch is 'main' install jupyter relate libs
if [ "$(git rev-parse --abbrev-ref HEAD)" == "main" ]; then
   pip install ipykernel
   pip install notebook
   python -m ipykernel install --user --name=venv --display-name "Python (venv)"
fi

echo ".venv created!"
