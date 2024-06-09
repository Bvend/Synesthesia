import numpy as np
import scipy.io.wavfile as wav


SAMPLE_RATE = 44100 # em Hz.
TIME_PER_SAMPLE = 1 / SAMPLE_RATE # em s.
TIME_PER_IMAGE = 10 # em s.
GAIN = -20 # em dB.
NUM_NOTES = 72
F_A440 = 440 # em Hz.
INDEX_A440 = 1 * 12 + 9 # considerando indexacao em 0 para a nota mais grave.

f = np.zeros(NUM_NOTES) # frequencias das notas, em Hz, deve ser pre-computado.


def compute_note_frequencies():
    for i in range(len(f)):
        f[i] = F_A440 * (2 ** ((i - INDEX_A440) / 12))


def fade_in_out(signal, fade_length = 1000):
    length = len(signal)
    fade_in = (1 - np.cos(np.linspace(0, np.pi, num = fade_length, endpoint = False))) * 0.5
    fade_out = np.flip(fade_in)

    for i in range(fade_length):
        signal[i] *= fade_in[i]
        signal[length - i - 1] *= fade_out[fade_length - i - 1]


def generate_signal(length, freq): # 'length' eh o numero de amostras.
    signal = np.zeros(length)
    t = 0
    for i in range(length):
        signal[i] = np.sin(2 * np.pi * freq * t)
        # signal[i] = 1 if np.sin(2 * np.pi * freq * t) >= 0 else -1
        t += TIME_PER_SAMPLE
        # Uma alternativa sem t:
        # signal[i] = np.sin(2 * np.pi * freq * i / SAMPLE_RATE)
    fade_in_out(signal)
    return signal


def add_signal(signal, output, start_idx):
    length = len(signal)
    for i in range(length):
        output[i + start_idx] += signal[i]


def adjust_volume(signal, gain):
    amplitude = 10 ** (gain / 20)
    signal *= amplitude


def clip_signal(signal):
    length = len(signal)
    for i in range(length):
        if signal[i] > 1:
            signal[i] = 1
        elif signal[i] < -1:
            signal[i] = -1


def generate_audio_from_notes(notes):
    # O ideal seria determinar dimensoes fixas para 'notes' e ter estes valores como constantes:
    num_cell_columns = len(notes[0])
    time_per_column = TIME_PER_IMAGE / num_cell_columns
    samples_per_cell = round(SAMPLE_RATE * time_per_column)

    output = np.zeros(samples_per_cell * num_cell_columns)
    for i in range(notes.shape[0]): # = NUM_NOTES, supostamente.
        cell_cnt = 0; start_cell_idx = 0
        for j in range(num_cell_columns):
            if notes[i, j] == 1:
                cell_cnt += 1
            else:
                if cell_cnt > 0:
                    # Considerar inverter para f[NUM_NOTES - i - 1].
                    signal = generate_signal(samples_per_cell * cell_cnt, f[NUM_NOTES - i - 1])
                    add_signal(signal, output, samples_per_cell * start_cell_idx)
                cell_cnt = 0
                start_cell_idx = j + 1
        if cell_cnt > 0:
            # Ver comentario acima.
            signal = generate_signal(samples_per_cell * cell_cnt, f[NUM_NOTES - i - 1])
            add_signal(signal, output, samples_per_cell * start_cell_idx)
    adjust_volume(output, GAIN)
    clip_signal(output)
    return output


def write_audio_file(audio_list):
    output = np.concatenate(audio_list)
    wav.write('/home/raspas/Codes/Synesthesia/source/output.wav', SAMPLE_RATE, output.astype(np.float32))
