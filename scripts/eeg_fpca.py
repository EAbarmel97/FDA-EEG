import os 
import re

import skfda.representation.basis as basis
from skfda.exploratory.visualization import FPCAPlot
from skfda.preprocessing.dim_reduction import FPCA
from skfda.representation.basis import BSplineBasis
from skfda.representation.interpolation import SplineInterpolation

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


def plot_fpca_and_functional_eeg(
    subject_file_path_dict: Dict[int, str],
    data_subdir_name: str,
    n_basis: int,
    write_eigspectra: bool = False
    ) -> None:
    """
    Plots both the funtional data obtained from eeg signals and its functional 
    principal components. If `write_eigspectra` is true a CSV file containing
    the eigenspectrum by subject is written under 'eigspectrum_data'
    """
    all_labels = list(label_index_dict.keys())

    if write_eigspectra:
        subject_eigspectrum_dict = {}

    if re.match(r"before", data_subdir_name):
        time_period = TimePeriod.BEFORE
    else:
        time_period = TimePeriod.AFTER

    for subject_idx in range(len(subject_file_path_dict)):
        eeg_data = eeg_dataclass(subject_idx, subject_file_path_dict, all_labels, time_period)
        
        eigspectrum = eeg_fpca(eeg_data,n_basis=n_basis,save_plot=True)
        subject_eigspectrum_dict[subject_idx] = eigspectrum
        
    if write_eigspectra: 
            df = pd.DataFrame(subject_eigspectrum_dict)
            csv_file_name = f"{time_period.value}_fpca_eigspectrum.csv"
                            
            df.to_csv(os.path.join("eigenspectrum", csv_file_name))              
    return 

def plot_eigspectra(data_subdir_name: str) -> None:
    if re.match(r"before", data_subdir_name):
        time_period = TimePeriod.BEFORE
    else:
        time_period = TimePeriod.AFTER
    
    eigspectra_data = pd.read_csv(f"eigenspectrum/{time_period.value}_fpca_eigspectrum.csv")
    for i in range(1, eigspectra_data.shape[1]):

        eigspectrum = eigspectra_data.iloc[:,i].values
        ranks = np.arange(1, len(eigspectrum)+1)
        slope, intercept, r, _, _ = stats.linregress(np.log10(ranks), np.log10(eigspectrum))

        vals = list(map(lambda x: 10**(intercept + np.log10(x)*slope) , ranks))
        plt.loglog(ranks, eigspectrum)
        plt.plot(ranks, vals, label=f'Fit: y = {10**intercept:.2f} * x^{slope:.2f}', color='red', linewidth=2)

        #label axes
        plt.xlabel('log-rank')
        plt.ylabel('log-eigval')
        plt.text(1, 1, f"$r^2 = {r**2:.3f}$", fontsize=12, color="black")
        plt.savefig(f"plots/eigenspectrum/{time_period.value}/subject{i}.pdf")
        plt.close()

            
before_arith_test = {0: '/home/enki/Documents/THESIS/FDA-EEG/data/eeg-during-mental-arithmetic-tasks-1.0.0/Subject00_1.edf',
                     1: '/home/enki/Documents/THESIS/FDA-EEG/data/eeg-during-mental-arithmetic-tasks-1.0.0/Subject01_1.edf', 
                     2: '/home/enki/Documents/THESIS/FDA-EEG/data/eeg-during-mental-arithmetic-tasks-1.0.0/Subject02_1.edf', 
                     3: '/home/enki/Documents/THESIS/FDA-EEG/data/eeg-during-mental-arithmetic-tasks-1.0.0/Subject03_1.edf', 
                     4: '/home/enki/Documents/THESIS/FDA-EEG/data/eeg-during-mental-arithmetic-tasks-1.0.0/Subject04_1.edf', 
                     5: '/home/enki/Documents/THESIS/FDA-EEG/data/eeg-during-mental-arithmetic-tasks-1.0.0/Subject05_1.edf'}

after_arith_test= {0: '/home/enki/Documents/THESIS/FDA-EEG/data/eeg-during-mental-arithmetic-tasks-1.0.0/Subject00_2.edf', 
                   1: '/home/enki/Documents/THESIS/FDA-EEG/data/eeg-during-mental-arithmetic-tasks-1.0.0/Subject01_2.edf', 
                   2: '/home/enki/Documents/THESIS/FDA-EEG/data/eeg-during-mental-arithmetic-tasks-1.0.0/Subject02_2.edf', 
                   3: '/home/enki/Documents/THESIS/FDA-EEG/data/eeg-during-mental-arithmetic-tasks-1.0.0/Subject03_2.edf', 
                   4: '/home/enki/Documents/THESIS/FDA-EEG/data/eeg-during-mental-arithmetic-tasks-1.0.0/Subject04_2.edf', 
                   5: '/home/enki/Documents/THESIS/FDA-EEG/data/eeg-during-mental-arithmetic-tasks-1.0.0/Subject05_2.edf'}
        
if __name__ == '__main__': 

    #plot functional data and its associated truncated functional principal components
    plot_fpca_and_functional_eeg(before_arith_test, "before", 19, write_eigspectra=True)
    plot_fpca_and_functional_eeg(after_arith_test, "after", 19, write_eigspectra=True)

    #plot truncated spectrum in log-log scale
    plot_eigspectra("before")
    plot_eigspectra("after")