import os 
import re

import pyedflib
import numpy as np 
import matplotlib.pyplot as plt
import skfda

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

def eeg_data_matrix(subject_idx, subject_edfsignal_dict):
    #check if there's a edf file for a given subject index
    if subject_edfsignal_dict.get(subject_idx,-1) == -1:
        raise KeyError
    #build data matrix
    with pyedflib.EdfReader(subject_edfsignal_dict[subject_idx]) as f:
        eeg_signals_arr = []
        for idx in range(f.signals_in_file):
            eeg_signal = f.readSignal(idx)
            eeg_signals_arr.append(eeg_signal)
        f.close()
        return np.matrix(eeg_signals_arr)
        
#raw eeg-signals transformed into functional data using 
#B-splines basis functions
def data_2_funcdata(data_matrix):
    freqs = []
    fd = skfda.FDataGrid(
            data_matrix=data_matrix,
            grid_points=freqs
        )
    
    return None

