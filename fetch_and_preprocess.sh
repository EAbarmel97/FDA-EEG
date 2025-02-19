#!/bin/bash
data_dir=$(pwd)"/data"
virtual_env=".venv/bin/activate"


#if data dir doesnt exit
if [ ! -d $(pwd)/"data" ]; then
  mkdir -p $data_dir/csv_data/{before_arith,after_arith}
fi

mkdir -p $data_dir/csv_data/{before_arith,after_arith}

#download EEG-data
if [ ! -f "$data_dir/eeg-during-mental-arithmetic-tasks-1.0.0.zip" ]; then
  curl -o "$data_dir/eeg-during-mental-arithmetic-tasks-1.0.0.zip" "https://physionet.org/static/published-projects/eegmat/eeg-during-mental-arithmetic-tasks-1.0.0.zip" 2> download.log
fi

# searach .zip file and unzip it 
for file in "$data_dir"/*; do
    case "$file" in
    *.zip)
      echo "unziping ..."
      unzip "$file" -d "$data_dir"
    esac
done

#check the total number of files downloaded is correct
echo "procesing EDF files ..."

#activate env and process EDF files to create CSV files
source "$virtual_env" && python3 scripts/edf_preprocess.py