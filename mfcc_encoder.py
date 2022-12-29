from nnAudio.Spectrogram import MFCC
import numpy as np

def melfcc(signal, sr):
    mfcc_obj = MFCC(sr=sr, n_mfcc=30)
    mfcc = mfcc_obj(signal)
    return mfcc