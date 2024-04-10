import numpy as np
import scipy.io.wavfile as wav


SAMPLE_RATE = 44100
DELTA_T = 1 / 44100
GAIN = -40
TIME_PER_IMAGE = 10

NUM_NOTES = 72
FREQ_A440 = 440
LIN_A440 = 45
f = np.zeros(NUM_NOTES)


def adjust_volume(signal, gain):
    amplitude = 10 ** (gain / 20)
    signal *= amplitude


def add_signals(signal, output, start_idx):
    length = len(signal)
    for i in range(length):
        output[i + start_idx] += signal[i]


def fade_in_out(signal, length, fade_length = 1000):
    fade_in = (1 - np.cos(np.linspace(0, np.pi, fade_length))) * 0.5
    fade_out = np.flip(fade_in)

    for i in range(fade_length):
        signal[i] *= fade_in[i]
        signal[length - i - 1] *= fade_out[fade_length - i - 1]


def generate_signal(length, freq):
    signal = np.zeros(length)
    t = 0
    for i in range(length):
        signal[i] = np.sin(2 * np.pi * freq * t)
        t += DELTA_T
    fade_in_out(signal, length)
    return signal


def generate_audio_from_notes(notes):
    num_interv = len(notes[0])
    time_per_interv = TIME_PER_IMAGE / num_interv
    samples_per_interv = round(time_per_interv * SAMPLE_RATE)
    output = np.zeros(samples_per_interv * num_interv)
    for i in range(notes.shape[0]):
        interv_len = 0; interv_start = 0
        for j in range(num_interv):
            if notes[i, j] == 1:
                interv_len += 1
            else:
                if interv_len > 0:
                    signal = generate_signal(samples_per_interv * interv_len, f[i])
                    add_signals(signal, output, interv_start * samples_per_interv)   
                interv_len = 0
                interv_start = j + 1
        if interv_len > 0:
            signal = generate_signal(samples_per_interv * interv_len, f[i])
            add_signals(signal, output, interv_start * samples_per_interv)
    adjust_volume(output, GAIN)
    return output


def calculate_note_frequencies():
    for i in range(len(f)):
        f[i] = FREQ_A440 * (2 ** ((i - LIN_A440) / 12))