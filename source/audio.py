import numpy as np
import scipy.io.wavfile as wav


TIME_PER_IMAGE = 3 # s
SAMPLE_RATE = 44100 # Hz
A440 = 440 # Hz
A440_Y =




# Aplica meia função cosseno para fade in e fade out
def fade_in_out(signal, length, fade_length = 1000):
    fade_in = (1 - np.cos(np.linspace(0, np.pi, fade_length))) * 0.5
    fade_out = np.flip(fade_in)

    for i in range(fade_length):
        signal[i] *= fade_in[i]
        signal[length - i - 1] *= fade_out[fade_length - i - 1]

f = 440 # Frequência da nota musical
t_total = 3
t_decorrido = 0

gain = -20 # Decibels
amplitude = 10 ** (gain / 20)

# Array de audio
output = np.zeros(t_total * sample_rate)
signal = np.zeros(t_total * sample_rate)

for i in range(sample_rate):
    signal[i] = amplitude * np.sin(2 * np.pi * 220 * t_decorrido)
    t_decorrido += 1 / sample_rate
#fade_in_out(signal, sample_rate)
for i in range(sample_rate):
    output[i] += signal[i]

for i in range(sample_rate):
    signal[i] = amplitude * np.sin(2 * np.pi * 440 * t_decorrido)
    t_decorrido += 1 / sample_rate
#fade_in_out(signal, sample_rate)
for i in range(sample_rate, 2 * sample_rate):
    output[i] += signal[i - sample_rate]

for i in range(sample_rate):
    signal[i] = amplitude * np.sin(2 * np.pi * 220 * t_decorrido)
    signal[i] += amplitude * np.sin(2 * np.pi * 440 * t_decorrido)
    t_decorrido += 1 / sample_rate
#fade_in_out(signal, sample_rate)
for i in range(2 * sample_rate, 3 * sample_rate):
    output[i] += signal[i - 2 * sample_rate]

#output = fade_in_out(output)

wav.write('sine.wav', sample_rate, output.astype(np.float32))
