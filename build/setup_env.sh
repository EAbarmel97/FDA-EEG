#!/usr/bin/sh
# create virtualenv
python3 -m venv ./.venv

#source the excutable
source ./.venv/bin/activate

#upgrade pip
pip install --upgrade pip


#add kernel to une inside dedicated jupiter virtualenv
pip install ipykernel
pip install notebook
pip install -r requirements.txt

#adding the virtual env to Jupiter
python -m ipykernel install --user --name=venv --display-name "Python (venv)"