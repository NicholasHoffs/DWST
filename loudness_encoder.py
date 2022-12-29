from librosa import A_weighting, stft, db_to_amplitude
from nnAudio import Spectrogram
import numpy as np

def loudness(signal):
    #find proper stft parameters
    power_squared = np.square(Spectrogram.STFT(signal))
    power_squared_linear = db_to_amplitude(power_squared)
    power_mean_log = np.log(np.mean(power_squared_linear)+(10**-5))

    return power_mean_log