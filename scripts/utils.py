import os
import re

import numpy as np
import pyedflib
import pandas as pd

import skfda
import skfda.representation.basis as basis
from skfda.exploratory.visualization import FPCAPlot
from skfda.preprocessing.dim_reduction import FPCA
from skfda.representation.basis import BSplineBasis
from skfda.representation.interpolation import SplineInterpolation

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

def write_data_frames(subject_file_path_dict,data_subdir):
    """
    write_data_frames persists under `data` CSV files obtained by concatenating all EEG-signals for 
    each EDF file. The CSV files have the same file stem as the corresponding EDF files
    """
    all_labels = list(label_index_dict.keys())

    for subject_idx in range(len(subject_file_path_dict)-1):
        #attributes now are columns, observations are rows
        transposed_data = eeg_data_matrix(subject_idx, subject_file_path_dict, all_labels).transpose()

        df = pd.DataFrame(transposed_data, columns=all_labels)
        base_name = os.path.basename(subject_file_path_dict[subject_idx])
        csv_base_name = re.sub(r".edf",".csv", base_name)
        df.to_csv(os.path.join("data", data_subdir, csv_base_name))


def convert_eeg_2fd(data_matrix,fs, n_basis):
    """
    convert_eeg_2fd converts a raw `data_matrix` into a functional datum. First constructs the discrete scikit-fda 
    functional representation and then transforms it into the truncated basis-funcion representation. 
    All EEG signals are assumed to have the same frecuency sampling. 
    """

    #functional data in dicrete format
    fd = skfda.FDataGrid(
            data_matrix=data_matrix,
            grid_points= np.linspace(0,data_matrix.shape[1], data_matrix.shape[1])/fs
        )

    #raw eeg-signals transformed into functional data using B-splines basis functions
    fd_basis = fd.to_basis(basis.BSplineBasis(n_basis=n_basis))
    return fd_basis