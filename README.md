# FDA-EEG data

Notebook containing functional data analysis applied to eeg signals from the publicly available Physionet [dataset](https://physionet.org/content/eegmat/1.0.0/) titled "EEG During Mental Arithmetic Tasks".

Finally regression analysis is applied to the approximation of the eigen-spectrum. To validate the hypotesis its powerlaw distributed a Kolmogorov-Smirnoff test is applied.

# Usage
From the terminal: 

1. Run: `bash build/setup_env.sh` (this may take a few minutes)
2. Launch the jupyter server: `bash launch_jupyter.sh`
