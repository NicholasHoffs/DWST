from librosa import A_weighting, db_to_amplitude, stft, fft_frequencies, load
import numpy as np
from torch import tensor, stft

def power_to_db(power, ref_db=0.0, range_db=80):
  """Converts power from linear scale to decibels."""
  

  # Convert to decibels.
  pmin = 10**-(range_db / 10.0)
  power = np.maximum(pmin, power)
  db = 10.0 * np.log10(power)

  # Set dynamic range.
  db -= ref_db
  db = np.maximum(db, -range_db)
  return db

def compute_loudness(audio,
                     sample_rate=16000,
                     hop_length=64,
                     n_fft=512,
                     range_db=80,
                     ref_db=0.0,
                     padding='center'):


# Temporarily a batch dimension for single examples.
  is_1d = (len(audio.shape) == 1)
  audio = audio[np.newaxis, :] if is_1d else audio

  # Take STFT.
  s = stft(audio, n_fft=n_fft, hop_length=hop_length)

  # Compute power.
  amplitude = np.abs(s).squeeze()
  amplitude = amplitude[:, :, :-1]
  power = amplitude**2

  # Perceptual weighting.
  frequencies = fft_frequencies(sr=sample_rate, n_fft=n_fft)
  a_weighting = A_weighting(frequencies)[np.newaxis, np.newaxis, :]
  # Perform weighting in linear scale, a_weighting given in decibels.
  weighting = 10**(a_weighting/10)
  power = power * weighting

  # Average over frequencies (weighted power per a bin).
  avg_power = np.mean(power, axis=-1)
  loudness = power_to_db(avg_power,
                              ref_db=ref_db,
                              range_db=range_db)

  return loudness

if __name__ == "__main__":
    y, sr = load('./test_audio/mallet_acoustic_074-072-050.wav')
    y=tensor(y)
    loudness = compute_loudness(y,sample_rate=sr)

    print(loudness.shape)