from loudness_encoder import loudness
from pitch_encoder import pitch
from mfcc_encoder import compute_z

from tqdm import tqdm
import numpy as np
import os
from librosa import load

from pandas import read_csv

# ROOT_DIRS = ['D:/NSynth/nsynth-train/audio','D:/NSynth/nsynth-valid/audio','D:/NSynth/nsynth-test/audio']
ROOT_DIR = 'D:/NSynth/nsynth-train/audio'
file_train = read_csv('./file_names/file_train_names.csv')

def preprocess(file_path, sampling_rate, n_fft, hop_size):
    signal, sr = load(file_path, sr=None)

    #pitch
    f0 = pitch(signal, sr, hop_size=hop_size, model_capacity='large')
    #loudness
    l = loudness(signal, sr, n_fft=n_fft, hop_length = hop_size)
    #z(MFCC)
    z = compute_z(signal, sample_rate=sr, n_mfcc=30, log_mel=True, n_fft=1024, hop_length=256, f_min=20,f_max=8000,center=True)

    np.save(file_path.replace('audio', 'pitch').replace('.wav','.npy'), f0)
    np.save(file_path.replace('audio', 'loudness').replace('.wav','.npy'), l)
    np.save(file_path.replace('audio', 'z').replace('.wav','.npy'), z)
    

if __name__ == '__main__':
    for ix, file in tqdm(file_train.iterrows()):
        file_path = os.path.join(ROOT_DIR, file[0]+'.wav')

        preprocess(file_path, 16000, 512, 128)