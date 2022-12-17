import numpy as np
from scipy.io.wavfile import write

#this creates a one cycle loop with any function
def create_wavetable(func, len, init_phase):
    wavetable = np.zeros((len,))
    for i in range(len):
        wavetable[i] = func(
            2*np.pi*i/len +
            2*np.pi*init_phase #this should be between 0 and 1, putting 1/2 is like pi because 2pi*phase
            )
    return wavetable

class Wavetable_Oscillator:
    def __init__(self, wavetable, freq, amp, sr, duration):
        self.wavetable=wavetable
        self.freq=freq
        self.amp=amp
        self.sr=sr
        self.duration = duration

        self.wavetable_len=np.shape(self.wavetable)[0]
        self.index_incremenent=self.wavetable_len*self.freq/self.sr

        self.data = self.sound_gen()
        
    #too dumb for this
    #@property
    #def freq(self):
    #    return self.freq

    #@freq.setter
    #def set_freq(self, freq):
    #    self.freq=freq
    #    self.index_increment=self.wavetable_len*self.freq/self.sr

    def get_sample(self, ix):
        
        
        #figure out to do w/ numpy - should be very easy
        value_low = self.wavetable[int(np.floor(ix)) % self.wavetable_len]
        value_high = self.wavetable[int(np.ceil(ix)) % self.wavetable_len] 

        value = (value_low+value_high)/2

        return value

    def sound_gen(self):
        output_len = self.sr*self.duration
        output = np.zeros(output_len)
        
        ix = 0

        for i in range(output_len):
            output[i]=self.get_sample(ix)
            ix+=self.index_incremenent 
        
        output = self.amp * output

        return output
def write_to_sound(path,sr,output):
    write(path, rate=sr, data=output)