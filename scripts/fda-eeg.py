import os 
import re

import pyedflib
import numpy as np 
import matplotlib.pyplot as plt

import skfda
import skfda.representation.basis as basis
from skfda.exploratory.visualization import FPCAPlot
from skfda.preprocessing.dim_reduction import FPCA
from skfda.representation.basis import BSplineBasis
from skfda.representation.interpolation import SplineInterpolation

from scipy import stats 

from utils import *

#NOTE: dataset needs to be downloaded and unziped  

#filter edf files
eeg_signalfiles_names = list(filter(lambda s : s.endswith(".edf") , 
                            [os.path.abspath(os.path.join("data/eeg-during-mental-arithmetic-tasks-1.0.0", f)) for 
                            f in os.listdir("data/eeg-during-mental-arithmetic-tasks-1.0.0")]
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

f = pyedflib.EdfReader(before_arith_task[0])

print(before_arith_task)
print(after_arith_task)

#print edf file metadata
print(f.file_info_long())
eeg_signal = f.readSignal(label_index_dict.get("P4", None))
f.close()
print()
print("eeg signal number 0: ", eeg_signal)

all_labels = list(label_index_dict.keys())
data = eeg_data_matrix(1, before_arith_task, all_labels)

n_basis = 19

#raw eeg-signals transformed into functional datum
fd_basis = convert_eeg_2fd(data, 500, n_basis)
print(fd_basis)