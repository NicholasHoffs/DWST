from nnAudio.Spectrogram import STFT
import numpy as np

def stft(signal, sample_rate, n_fft=2048, hop_length=None, window_length = 2048):
    hop_length = window_length//4
    stft_obj = STFT(n_fft=n_fft,win_length=window_length,hop_length=hop_length, center=True, output_format='Complex')
    stft_val = stft_obj(signal)

    return stft_val

