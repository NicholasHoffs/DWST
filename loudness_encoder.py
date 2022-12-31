from librosa import perceptual_weighting, db_to_amplitude
from utils import stft
from nnAudio.librosa_functions import fft_frequencies
import numpy as np
from torch import tensor



def loudness(signal, sample_rate, n_fft=2048, hop_length=None, window_length = 2048):
    signal = tensor(signal)
    hop_length=window_length//4
    #find proper stft parameters
    spec = stft(signal, sample_rate, n_fft, window_length=window_length).abs()
    fft_freq = fft_frequencies(sample_rate, n_fft)
    spec = spec[:,:,:,:-1]
    spec = spec.squeeze()

    # print("Spectogram size: {}\n FFT_Freq size: {}".format(np.shape(spec), np.shape(fft_freq)))
    adj_spec = perceptual_weighting(spec**2, fft_freq)
    adj_linear_spec = db_to_amplitude(adj_spec)
    mean = np.mean(adj_linear_spec, axis=0)
    print(np.shape(mean))
    #small addition prevents overflow
    compressed_mean = np.log10(mean+10**(-5))

    return compressed_mean
