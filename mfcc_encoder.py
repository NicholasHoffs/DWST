import numpy as np
from torch import tensor
from torchaudio.transforms import MFCC
from torchaudio import load

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm


def compute_z(signal, sample_rate, n_mfcc, log_mel, n_fft, hop_length, f_min, f_max, center):
    """
    Values used in paper are sample_rate=16000, n_mfcc=30, log_mel=True, n_fft=1024, hop_length=256, f_min=20Hz, f_max=8000Hz, center=True
    """

    mfcc_transform = MFCC(sample_rate=sample_rate,n_mfcc=n_mfcc,log_mels=True,melkwargs={"n_fft":n_fft, "hop_length":hop_length, "n_mels":128, "f_min":f_min, "f_max":f_max,"center":center})
    mfcc = mfcc_transform(y).squeeze()
    #Shape is now (30,251) - trim last time step to 250
    mfcc = mfcc[..., :-1]
    print('MFCC Shape: {}'.format(mfcc.shape))
    return mfcc