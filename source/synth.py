import numpy as np
import scipy.io.wavfile as wav

sample_rate = 44100
delta_t = 1 / 44100
gain = -20 # Decibels

# Aplica meia função cosseno para fade in e fade out
def fade_in_out(signal, length, fade_length = 1000):
    fade_in = (1 - np.cos(np.linspace(0, np.pi, fade_length))) * 0.5
    fade_out = np.flip(fade_in)

    for i in range(fade_length):
        signal[i] *= fade_in[i]
        signal[length - i - 1] *= fade_out[fade_length - i - 1]

def generate_signal(length, freq, current_t, delta_t):
    signal = np.zeros(length)
    current_t_aux = current_t
    for i in range(length):
        signal[i] = np.sin(2 * np.pi * freq * current_t_aux)
        current_t_aux += delta_t
    fade_in_out(signal, length)

def adjust_volume(signal, volume_db):
    amplitude = 10 ** (gain / 20)
    signal *= amplitude

#def generate_audio_from_page(notes, sample_rate, total_t, current_t, gain):
#    current_t_aux = current_t
#    signal = np.zeros(total_t * sample_rate)
#    num_interv = len(notes[0])
#    for i in notes:
#        interv_len = 0
#        for j in num_interv:
#            if 
#    adjust_volume(signal, gain)
#    return signal
        

total_t = 3
current_t = 0

# Array de audio
output = np.zeros(total_t * sample_rate)
signal = np.zeros(total_t * sample_rate)

wav.write('sine.wav', sample_rate, output.astype(np.float32))