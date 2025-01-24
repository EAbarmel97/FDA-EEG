import numpy as np
import pyedflib
import pandas as pd

label_index_dict = {"Fp1":0,"Fp2":1,"F3":2,"F4":3,"F7":4,"F8":5,"T3":6,"T4":7,"C3":8,
                    "C4":9,"T5":10,"T6":11,"P3":12,"P4":13,"O1":14,"O2":15,"Fz":16, "Cz":17,"Pz":18}

def eeg_data_matrix(subject_idx, subject_edfsignal_dict, labels):
    #check if there's a edf file for a given subject index
    if subject_edfsignal_dict.get(subject_idx,-1) == -1:
        raise KeyError
    
    #build data matrix
    with pyedflib.EdfReader(subject_edfsignal_dict[subject_idx]) as f:
        eeg_signals_arr = []
        for label in labels:
            idx = label_index_dict.get(label,-1)
            if idx == -1:
               raise KeyError
            eeg_signal = f.readSignal(idx)
            eeg_signals_arr.append(eeg_signal)

        f.close()
        return np.matrix(eeg_signals_arr)

def write_data_frames(subject_file_path_dict):
    for subject_idx in range(len(subject_file_path_dict.keys())-1):
        all_labels = list(label_index_dict.keys())
        data = eeg_data_matrix(subject_idx, subject_file_path_dict, all_labels)
        