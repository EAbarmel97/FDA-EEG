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

import os 
import re

from utils import *

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


def do_for_dir(
    subject_file_path_dict: Dict[int, str],
    fun: callable
) -> None:
    for subject_idx in range(len(subject_file_path_dict)-1):
        pass

if __name__ == '__main__':
    #save plots of the functional representation of the EEG data
    
    #save plots of the fpca associated with the functional EEG data
    
    #save eigenvalues obtained from truncated FPCA
    
    print("ploting...")