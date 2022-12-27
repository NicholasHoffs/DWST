import os

from torch.utils.data import Dataset
from torchaudio import load
import pandas as pd

FILE_NAMES = "./file_train_names.csv"
ROOT_DIR = "D:\\NSynth\\nsynth-train\\audio"

class NSynth(Dataset):

    def __init__(self, file_names, root_dir):
        self.file_names = pd.read_csv(file_names)
        self.root_dir = root_dir

    def _get_file_path(self, index):
        return os.path.join(self.root_dir, self.file_names.iloc[index][0]+'.wav',)
    
    def _load_sample(self, path):
        signal, sr = load(path)
        return signal, sr 

    def __getitem__(self, index):
        file_path = self._get_file_path(index)
        signal, sr = self._load_sample(file_path)
        return signal, sr

    def __len__(self):
        return len(self.file_names.iloc[:,0])

if __name__ == "__main__":
    nsynth = NSynth(FILE_NAMES, ROOT_DIR)

    print("Length of nsynth dataset is {} samples\n".format(len(nsynth)))
    print("Info of third sample is {}".format(nsynth[2]))