# just ignore this k

from synthesizer import *
from composer import *
from plotter import *


import numpy as np

# f = F[39]
t = 1
f = F[5] # F[58]

a = generate_adsr_envelope(t, min(0.01, 0.005 * t), min(0.04, 0.02 * t), 0.5, 0.975 * t)
e = generate_adsr_envelope(t, min(0.01, 0.005 * t), 0, 1, 0.025 * t)

# for i in range(3, 20):
#     x = a * generate_fm_wave(t, f, f, i)
#     plot_frequency(f'../resources/samples/tmp/plots/piano{i}.png', x,
#                    in_db= True, r_hz = 1000)
#     x = amplify_signal(x, GAIN_DB)
#     write_wav(f'../resources/samples/tmp/piano{i}.wav', x)

x = generate_square_wave(t, f)
x = amplify_signal(x, GAIN_DB)
write_wav(f'../resources/samples/tmp/square.wav', x)

x = generate_sawtooth_wave(t, f)
x = amplify_signal(x, GAIN_DB)
write_wav(f'../resources/samples/tmp/sawtooth.wav', x)


notes = []
for i in range(len(F)):
    x = synthetize_strings(t, F[i])
    x = a * 1.5 * generate_fm_wave(t, F[i], F[i], 3 - 2.7 * e)
    # x += a * 1.5 * generate_fm_wave(t, 3 * F[i], 2 * F[i], 1)
    # x += 0.33 * a * generate_fm_wave(t, 2 * F[i], 5 * F[i], 10 * e)
    x = amplify_signal(x, GAIN_DB)
    notes.append(x)
x = np.concatenate(notes)
write_wav(f'../resources/samples/tmp/piano.wav', x)


# x = read_wav('../resources/samples/piano.wav')[:, 1]

# # x = np.mean(x, axis = 1)

# BEGIN = int(np.round(2.75 * FS_HZ))
# DUR = int(np.round(0.49 * FS_HZ))
# END = BEGIN + DUR

# x = x[BEGIN : END]

# plot_waveform('../resources/samples/piano_wave.png', x)
# plot_frequency('../resources/samples/piano_freq.png', x,
#                in_db = True, r_hz = 1000)
# write_wav('../resources/samples/piano_cut.wav', x)
