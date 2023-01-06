import numpy as np
from scipy.io.wavfile import write
import torch.nn as nn
import torch
from torch.nn import TransformerDecoder

def create_wavetable(func, len, init_phase, freq):
    wavetable = np.zeros((len,))
    for i in range(len):
        wavetable[i] = func(
            freq * 2*np.pi*i/len +
            2*np.pi*init_phase 
            )
    return torch.tensor(wavetable)

def full_oscillator(wt, freq, sample_rate, duration):
    index_increment = wt.shape[0]*freq/sample_rate
    n_samples = sample_rate*duration
    indices = torch.arange(0,sample_rate*duration*index_increment, index_increment)
    indices = indices % wt.shape[0]
    low = torch.floor(indices.clone()).long()
    frac_ix = indices-low

    return wt[low] + frac_ix*(wt[(low+1) % wt.shape[0]]-wt[low])

class Wavetable_Synth(nn.Module):
    #can use pre-defined wavetables or not
    def __init__(self, sample_rate=16000, wt=None, n_wt = 20, wt_len=512,  duration=4):
        super(Wavetable_Synth, self).__init__()
        self.sample_rate = sample_rate
        self.wt = [] if wt is None else wt
        self.n_wt = n_wt
        self.wt_len = wt_len

        #DO TRANSFORMER DECODER ON PHASE AND AMPLITUDE

        self.TransformerDecoder

        for _ in range(n_wt):
                cur = nn.Parameter(torch.empty(self.wt_len).normal_(mean=0, std=0.01))
                self.wt.append(cur)

        self.wt = nn.ParameterList(self.wt)

        if self.wt == None:
            for i in range(n_wt):
                if i==0:
                    self.wt[i] = create_wavetable(np.sin, wt_len, np.random.uniform(0,1), 1)
                    self.wt[i] = self.append_first_to_end(self.wt[i])
                    self.wt.require
                elif i==1:
                    self.wt[i] = create_wavetable(np.sin, wt_len, np.random.uniform(0,1), 2)
                    self.wt[i] = self.append_first_to_end(self.wt[i])                    
                elif i==2:
                    self.wt[i] = create_wavetable(np.sin, wt_len, np.random.uniform(0,1), 3)
                    self.wt[i] = self.append_first_to_end(self.wt[i])
                elif i==3:
                    self.wt[i] = create_wavetable(np.sin, wt_len, np.random.uniform(0,1), 4)
                    self.wt[i] = self.append_first_to_end(self.wt[i])

                else:
                    self.wt[i] = self.append_first_to_end(self.wt[i])
    
    def append_first_to_end(self, wt):
        return torch.cat([wt[:-1], wt[0].unsqueeze(-1)], dim=-1)

    def forward(self, pitch, amp):
        pass

    # def forward(self, pitch, amplitude):
            

if __name__ == '__main__':
    wt = create_wavetable(np.sin, 512, 0, 1)

    output = full_oscillator(wt, 440, 16000, 3)
    output = np.array(output)
    write('./test_audio/test_oscillator.wav',16000, output)