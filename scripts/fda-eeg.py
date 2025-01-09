import os

import pyedflib
import numpy as np


eeg_signalfiles_names = os.listdir("../data/eeg-during-mental-arithmetic-tasks-1.0.0")

eeg_signal = pyedflib.EdfReader.readSignal(0,0,1)