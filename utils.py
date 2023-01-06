from nnAudio.Spectrogram import STFT
import numpy as np

def stft(signal, sample_rate, n_fft=2048, hop_length=512, center=True):
    stft_obj = STFT(n_fft, hop_length=hop_length, center=center)
    stft_val = stft_obj(signal)

    return stft_val

