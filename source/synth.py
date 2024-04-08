import numpy as np
import scipy.io.wavfile as wav

sample_rate = 44100
f = 220 # frequência da nota musical
t_total = 3
t_decorrido = 0

# array de audio
output = np.zeros(t_total * sample_rate) 

for i in range(t_total * sample_rate):
    output[i] = np.sin(2 * np.pi * f * t_decorrido)
    t_decorrido += 1 / sample_rate

wav.write('sine.wav', sample_rate, output.astype(np.float32))

"""
samplerate = 44100
f = 440
t = 3
waveform = np.sin

wavetable_length = 64
wave_table = np.zeros((wavetable_length,))

#for n in range(wavetable_length):
#    wave_table[n] = waveform(2 * np.pi * n / wavetable_length)

output = np.zeros((t * samplerate,))

index = 0
indexIncrement = f * wavetable_length / samplerate
realt = 0
for n in range(output.shape[0]):
    output[n] = waveform(2 * np.pi * realt * f)
    realt += 1. / samplerate
    #index += indexIncrement
    #index %= wavetable_length

wav.write('sine.wav', samplerate, output.astype(np.float32))
"""