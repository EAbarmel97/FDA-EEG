#!/bin/bash
fda_eeg="/storage5/eabarmel/FDA-EEG"
virtual_env="$fda_eeg/.venv/bin/activate"

data_dir="$(dirname "$0")/data"

#if data dir doesnt exist create it with all its subdirs
if [ ! -d "$data_dir" ]; then
  mkdir -p $data_dir/csv_data/{before_arith,after_arith}
fi
#create subdirs inside data/ 
mkdir -p $data_dir/csv_data/{before_arith,after_arith}

#download EEG-data
if [ ! -f "$data_dir/eeg-during-mental-arithmetic-tasks-1.0.0.zip" ]; then
  curl -o "$data_dir/eeg-during-mental-arithmetic-tasks-1.0.0.zip" "https://physionet.org/static/published-projects/eegmat/eeg-during-mental-arithmetic-tasks-1.0.0.zip" 2> ./download.log
fi

if [ ! -d "$data_dir/eeg-during-mental-arithmetic-tasks-1.0.0" ]; then
  # search .zip file and unzip it 
  for file in "$data_dir"/*; do
      case "$file" in
      *.zip)
        echo "unziping ..."
        unzip "$file" -d "$data_dir"
      esac
  done
fi

echo "procesing EDF files ..."

#activate env and process EDF files to create CSV files
source "$virtual_env" && python3 "$fda_eeg"/scripts/edf_preprocess.py