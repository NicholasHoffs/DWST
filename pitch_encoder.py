from crepe import predict
import numpy as np

def pitch(signal, sampling_rate, hop_size, model_capacity="full"):
    length = signal.shape[-1] // hop_size
    f0 = predict(
        signal,
        sampling_rate,
        step_size=int(1000 * hop_size / sampling_rate),
        verbose=1,
        center=True,
        viterbi=True,
        model_capacity="medium"
    )
    f0 = f0[1].reshape(-1)[:-1]

    if f0.shape[-1] != length:
        f0 = np.interp(
            np.linspace(0, 1, length, endpoint=False),
            np.linspace(0, 1, f0.shape[-1], endpoint=False),
            f0,
        )

    return f0