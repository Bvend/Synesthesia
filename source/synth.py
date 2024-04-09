import numpy as np
import scipy.io.wavfile as wav

# Aplica meia função cosseno para fade in e fade out
def fade_in_out(signal, fade_length = 1000):
    fade_in = (1 - np.cos(np.linspace(0, np.pi, fade_length))) * 0.5
    fade_out = np.flip(fade_in)

    for i in range(fade_length):
        signal[i] *= fade_in[i]
        signal[len(signal) - i - 1] *= fade_out[fade_length - i - 1]

    return signal

sample_rate = 44100
f = 440 # Frequência da nota musical
t_total = 3
t_decorrido = 0

gain = -20 # Decibels
amplitude = 10 ** (gain / 20)

# Array de audio
output = np.zeros(t_total * sample_rate)

for i in range(t_total * sample_rate):
    output[i] = amplitude * np.sin(2 * np.pi * f * t_decorrido)
    t_decorrido += 1 / sample_rate

output = fade_in_out(output)

wav.write('sine_fade.wav', sample_rate, output.astype(np.float32))