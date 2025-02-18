import os
import re
from dataclasses import dataclass
from typing import Dict, List
from enum import Enum

import numpy as np
import pyedflib
import pandas as pd
import matplotlib.pyplot as plt
import skfda
import skfda.representation.basis as basis

from skfda.exploratory.visualization import FPCAPlot
from skfda.preprocessing.dim_reduction import FPCA
from skfda.representation.basis import BSplineBasis
from skfda.representation.interpolation import SplineInterpolation


label_index_dict = {"Fp1":0,"Fp2":1,"F3":2,"F4":3,"F7":4,"F8":5,"T3":6,"T4":7,"C3":8,
                    "C4":9,"T5":10,"T6":11,"P3":12,"P4":13,"O1":14,"O2":15,"Fz":16, "Cz":17,"Pz":18}

class TimePeriod(Enum):
    BEFORE = "before"
    AFTER = "after"
@dataclass
class EEGData:
        subject_id: int
        data_matrix: np.matrix
        fs_eeg_signals: np.float64
        time_period: TimePeriod


def eeg_dataclass(
    subject_idx: int, 
    subject_edfsignal_dict: Dict[int, str], 
    labels: List[str],
    time_period: TimePeriod
    ) -> EEGData:
    if subject_edfsignal_dict.get(subject_idx,-1) == -1:
        raise KeyError
    
    #concatenate eeg signals into a data matrix
    with pyedflib.EdfReader(subject_edfsignal_dict[subject_idx]) as f:
        eeg_signals_arr = []
        for label in labels:
            idx = label_index_dict.get(label,-1)
            if idx == -1:
               raise KeyError
            eeg_signal = f.readSignal(idx)
            eeg_signals_arr.append(eeg_signal)
        sample_fs = f.getSampleFrequencies()
        f.close()
        data_matrix = np.matrix(eeg_signals_arr)

        #build dataclass instance
        eeg_data = EEGData(
        subject_id=subject_idx,
        data_matrix= data_matrix,
        fs_eeg_signals=sample_fs[0],
        time_period = time_period
        )    
        return eeg_data

def write_data_frames(
    subject_file_path_dict: Dict[int, str],
    data_subdir_name: str
    ) -> None:
    """
    write_data_frames persists under `data` CSV files obtained by concatenating all EEG-signals for 
    each EDF file. The CSV files have the same file stem as the corresponding EDF files
    """
    all_labels = list(label_index_dict.keys())

    if re.match(r"before", data_subdir_name):
        time_period = TimePeriod.BEFORE
    else:
        time_period = TimePeriod.AFTER

    for subject_idx in range(len(subject_file_path_dict)-1):
        #attributes now are columns, observations are rows
        eeg_data = eeg_dataclass(subject_idx, subject_file_path_dict, all_labels, time_period)
        transposed_data = eeg_data.data_matrix.transpose()

        df = pd.DataFrame(transposed_data, columns=all_labels)
        df["subject_idx"] = np.full_like(df.index,eeg_data.subject_id)
        df["fs"] = np.full_like(df.index,eeg_data.fs_eeg_signals)

        base_name = os.path.basename(subject_file_path_dict[subject_idx])
        csv_base_name = re.sub(r".edf",".csv", base_name)
        
        df.to_csv(os.path.join("data/csv_data", data_subdir_name, csv_base_name))


def convert_raweeg_2fd(
    eeg_data: EEGData, 
    n_basis: int, 
    save_plot: bool = False
    ) -> skfda.FDataBasis:
    """
    convert_eeg_2fd converts a raw `data_matrix` into a functional datum. First constructs the discrete scikit-fda 
    functional representation and then transforms it into the truncated basis-funcion representation. 
    All EEG signals are assumed to have the same frecuency sampling. 
    """
    data_matrix=eeg_data.data_matrix
    #functional data in dicrete format
    fd = skfda.FDataGrid(
            data_matrix= data_matrix,
            grid_points= np.linspace(0,data_matrix.shape[1], data_matrix.shape[1])/eeg_data.fs_eeg_signals
        )

    #raw eeg-signals transformed into functional data using B-splines basis functions
    fd_basis = fd.to_basis(basis.BSplineBasis(n_basis=n_basis))
    
    if save_plot:
        fd_basis.plot()
        if eeg_data.time_period.value == "before":
            plt.savefig(f"plots/raw2fd/before/subject{eeg_data.subject_id}.pdf")
        else:
            plt.savefig()
    return fd_basis

def eeg_fpca_eigspectrum(
    eeg_data: EEGData, 
    n_basis: int, 
    saveplot: bool = False
    ) -> np.ndarray:
    fd_basis = convert_raweeg_2fd(eeg_data, n_basis)
    fpca = FPCA(n_basis)
    fpca.fit(fd_basis)

    eigvals = np.square(fpca.singular_values_)
    return eigvals[np.abs(eigvals) >= np.finfo(float).eps]