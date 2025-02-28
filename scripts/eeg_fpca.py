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
            if not os.path.exists("./eigenspectrum"):
                os.makedirs("./eigenspectrum")
            df.to_csv(os.path.join("eigenspectrum", csv_file_name))              
    return 

def plot_eigspectra(data_subdir_name: str, write_expoenents: bool = False) -> None:
    """
    Plots the eigenspectra. If `write_expoenents` is True, writes a CSV file containing the OLS estimator 
    for the slope for each eigenspectrum
    """
    if re.match(r"before", data_subdir_name):
        time_period = TimePeriod.BEFORE
    else:
        time_period = TimePeriod.AFTER
    if write_expoenents:
        subject_slope_df = pd.DataFrame(columns=["subject_idx", "exponent"])
        
    eigspectra_data = pd.read_csv(f"eigenspectrum/{time_period.value}_fpca_eigspectrum.csv")
    for i in range(1, eigspectra_data.shape[1]):

        eigspectrum = eigspectra_data.iloc[:,i].values
        ranks = np.arange(1, len(eigspectrum)+1)

        # Try fits dropping up to max_dropped eigenvalues in the tail
        max_dropped = 5
        best_r2 = float("-inf")
        best_slope = None
        best_intercept = None
        fitted_ranks = None
        for num_drop in range(max_dropped+1):
            slope, intercept, r, _, _ = stats.linregress(np.log10(ranks[:len(ranks)-num_drop]), np.log10(eigspectrum[:len(ranks)-num_drop]))
            if r**2 > best_r2:
                best_r2 = r**2
                best_slope = slope
                best_intercept = intercept
                fitted_ranks = ranks[:len(ranks)-num_drop]
        r2 = best_r2
        slope = best_slope
        intercept = best_intercept
        
        if write_expoenents:
            subject_idx_slope = pd.DataFrame({"subject_idx": [i] ,"exponent": [slope]}).dropna(axis=1, how='all')
            subject_idx_slope = subject_idx_slope.dropna(axis=1, how='all')
            subject_slope_df = pd.concat([subject_slope_df, subject_idx_slope], ignore_index=True)


        vals = list(map(lambda x: 10**(intercept + np.log10(x)*slope) , fitted_ranks))
        plt.loglog(ranks, eigspectrum)
        plt.plot(fitted_ranks, vals, label=f'Fit: y = {10**intercept:.2f} * x^{slope:.2f}', color='red', linewidth=2)

        #label axes
        plt.xlabel('log-rank')
        plt.ylabel('log-eigval')
        plt.text(1, 1, f"$r^2 = {r2:.3f}$", fontsize=12, color="black")
   
        plt.title(f"FPCA exponent = {slope:.3f}")
        plt.tight_layout()
        plt.savefig(f"plots/eigenspectrum/{time_period.value}/{time_period.value}_subject{i}.png")
        plt.close()

    if write_expoenents:
        subject_slope_df.to_csv(os.path.join("eigenspectrum", "fit", f"{time_period.value}_slope.csv"))    

before_arith_test = {0: 'data/eeg-during-mental-arithmetic-tasks-1.0.0/Subject00_1.edf',
                     1: 'data/eeg-during-mental-arithmetic-tasks-1.0.0/Subject01_1.edf', 
                     2: 'data/eeg-during-mental-arithmetic-tasks-1.0.0/Subject02_1.edf', 
                     3: 'data/eeg-during-mental-arithmetic-tasks-1.0.0/Subject03_1.edf', 
                     4: 'data/eeg-during-mental-arithmetic-tasks-1.0.0/Subject04_1.edf', 
                     5: 'data/eeg-during-mental-arithmetic-tasks-1.0.0/Subject05_1.edf'}

after_arith_test= {0: 'data/eeg-during-mental-arithmetic-tasks-1.0.0/Subject00_2.edf', 
                   1: 'data/eeg-during-mental-arithmetic-tasks-1.0.0/Subject01_2.edf', 
                   2: 'data/eeg-during-mental-arithmetic-tasks-1.0.0/Subject02_2.edf', 
                   3: 'data/eeg-during-mental-arithmetic-tasks-1.0.0/Subject03_2.edf', 
                   4: 'data/eeg-during-mental-arithmetic-tasks-1.0.0/Subject04_2.edf', 
                   5: 'data/eeg-during-mental-arithmetic-tasks-1.0.0/Subject05_2.edf'}


if __name__ == '__main__': 

    #plot functional data and its associated truncated functional principal components
    plot_fpca_and_functional_eeg(before_arith_test, "before", 19, write_eigspectra=True)
    plot_fpca_and_functional_eeg(after_arith_test, "after", 19, write_eigspectra=True)

    #plot truncated spectrum in log-log scale
    plot_eigspectra("before", write_expoenents=True)
    plot_eigspectra("after", write_expoenents=True)
    
    #merge csvs
    if os.path.exists("eigenspectrum/fit/before_slope.csv") and os.path.exists("eigenspectrum/fit/after_slope.csv"):
        before = pd.read_csv("eigenspectrum/fit/before_slope.csv")
        after = pd.read_csv("eigenspectrum/fit/after_slope.csv")

        before_after_slope = pd.merge(before, after, on='subject_idx', how='outer').drop(columns=['Unnamed: 0_x', 'Unnamed: 0_y'])
        before_after_slope.to_csv(os.path.join("eigenspectrum", "fit","before_after_slope.csv"))  