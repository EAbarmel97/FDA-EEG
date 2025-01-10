import os 
import re

import pyedflib
import numpy as np 
import matplotlib.pyplot as plt

#NOTE: dataset needs to be downloaded and unziped  

#filter edf files
eeg_signalfiles_names = list(filter(lambda s : s.endswith(".edf") , 
                            [os.path.abspath(os.path.join("../data/eeg-during-mental-arithmetic-tasks-1.0.0", f)) for 
                            f in os.listdir("../data/eeg-during-mental-arithmetic-tasks-1.0.0")]
                        ))

#dicts with subject_id - eeg_signal_filepath
before_arith_task = {}
after_arith_task = {}


# process each file
for edf_file_name in eeg_signalfiles_names :
    file_name = os.path.basename(edf_file_name)
    
    # extract subject identifier and suffix
    if "_1.edf" in file_name:
        subject_id = int(re.findall(r"\d\d", file_name)[0])
        before_arith_task[subject_id] = edf_file_name
    
    elif "_2.edf" in file_name:
        subject_id = int(re.findall(r"\d\d", file_name)[0])
        after_arith_task[subject_id] = edf_file_name

f = pyedflib.EdfReader(before_arith_task[1])
print(f.signals_in_file) 
eeg_signal = f.readSignal(0)

print(eeg_signal)
