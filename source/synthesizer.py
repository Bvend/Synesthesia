# module dedicated to generating and processing one-dimensional signals, and
# inputting/outputting audio.
# for the composition of the audio track, check composer.


import numpy as np
from scipy.signal import convolve
from scipy.io import wavfile
import pygame
from pygame.locals import *


AUDIO_DIR = '../resources/audio/' # directory for audio input/output.

FS_HZ = 48000 # sample rate. standard choices are 44.1 kHz and 48 kHz.


def generate_impulse(len_s, delay_s = 0):
    n = np.arange(len_s * FS_HZ) # sample indices array [0 1 2 3 ...].
    x = np.where(n == np.round(delay_s * FS_HZ), 1., 0.)
    return x


def generate_step(len_s, delay_s = 0):
    n = np.arange(len_s * FS_HZ)
    x = np.where(n >= delay_s * FS_HZ, 1., 0.)
    return x


def generate_sine_wave(len_s, f_hz, ph_rad = 0):
    n = np.arange(len_s * FS_HZ)
    x = np.sin(ph_rad + (2 * np.pi * f_hz / FS_HZ) * n)
    return x


def generate_triangle_wave(len_s, f_hz, ph_rad = 0):
    n = np.arange(len_s * FS_HZ)
    x = (2 / np.pi) * np.arcsin(np.sin(ph_rad + (2 * np.pi * f_hz / FS_HZ) * n))
    return x


def generate_square_wave(len_s, f_hz, ph_rad = 0):
    n = np.arange(len_s * FS_HZ)
    x = np.where(np.sin(ph_rad + (2 * np.pi * f_hz / FS_HZ) * n) >= 0, 1., -1.)
    return x


def generate_sawtooth_wave(len_s, f_hz, ph_rad = 0):
    n = np.arange(len_s * FS_HZ)
    x = (2 / np.pi) * np.arctan(np.tan(ph_rad + (np.pi * f_hz / FS_HZ) * n))
    return x


def generate_fm_wave(len_s, fc_hz, fm_hz, i):
    # frequency modulation applied to sound synthesis allows for generating
    # complex waveforms from simple parameter choices.
    # when fc / fm is a rational p / q (irreducible), the wave's fundamental
    # frequency is fc / p = fm / q, and the side frequencies are harmonics;
    # otherwise, all frequencies are inharmonics.
    # i, the modulation index, scatters frequency strength on a wider band when
    # increased, being roughly linear on the number of side frequencies desired.
    # most remarkably, making i a function of time allows for dynamic spectrum
    # control, which is not easily achieved by convolution based filtering.
    # more information at:
    # https://en.wikipedia.org/wiki/Frequency_modulation_synthesis
    # https://web.eecs.umich.edu/~fessler/course/100/misc/chowning-73-tso.pdf

    n = np.arange(len_s * FS_HZ)
    m = np.sin((2 * np.pi * fm_hz / FS_HZ) * n) # modulating signal.
    c = np.sin((2 * np.pi * fc_hz / FS_HZ) * n + i * m) # carrier signal.
    return c


def generate_adsr_envelope(len_s, a_s, d_s, s_amp, r_s):
    # attack: time taken from 0 to 1;
    # decay: time taken from 1 to sustain amplitude;
    # sustain: amplitude (in [0, 1]) maintained following decay until release;
    # release: time taken from sustain amplitude to 0.

    num_a = int(np.round(a_s * FS_HZ))
    num_d = int(np.round((a_s + d_s) * FS_HZ)) - num_a
    num_s = int(np.round((len_s - r_s) * FS_HZ)) - (num_a + num_d)
    num_r = int(np.ceil(len_s * FS_HZ)) - (num_a + num_d + num_s)
    xa = np.linspace(0, 1, num = num_a, endpoint = False)
    xd = np.linspace(1, s_amp, num = num_d, endpoint = False)
    xs = np.full(num_s, s_amp)
    xr = np.linspace(s_amp, 0, num = num_r, endpoint = False)
    x = np.concatenate((xa, xd, xs, xr))
    return x


def generate_sinc_filter(fc_hz):
    # the sinc function in time is the rectangle function in frequency: it would
    # behave as the ideal low-pass filter if modelled as infinite.
    # truncating it results in ringing in the frequency domain, which is reduced
    # by a window function. here the blackman window is chosen.
    # more information at: http://www.dspguide.com/CH16.PDF

    n = np.arange(-(FS_HZ / 2) + 0.5, FS_HZ / 2 + 0.5)
    x = (2 * fc_hz) * np.sinc((2 * fc_hz / FS_HZ) * n) * np.blackman(FS_HZ)
    return x


def amplify_signal(x, gain_db):
    gain_amp = 10 ** (gain_db / 20)
    # formula clarification:
    # by definition, (sound) level_db = 10 * log10(intensity / intensity_ref),
    # and (sound) intensity is proportional to (pressure) amplitude ^ 2,
    # thus, level_db = 20 * log10(amplitude / amplitude_ref);
    # since gain_amp = amplitude_out / amplitude_in,
    # gain_amp = 10 ^ ((level_out_db - level_in_db) / 20).

    x = np.clip(gain_amp * x, -1, 1)
    return x


def filter_signal(x, f):
    x = convolve(x, f, mode = 'same') / sum(f)
    return x


def synthesize_blue(len_s, f_hz):
    a = generate_adsr_envelope(len_s, min(0.01, 0.005 * len_s),
                               min(0.04, 0.02 * len_s),0.5, 0.975 * len_s)
    e = generate_adsr_envelope(len_s, min(0.01, 0.005 * len_s),
                               0, 1, 0.025 * len_s)
    x = a * generate_fm_wave(len_s, f_hz, f_hz, 3 - 2.7 * e)
    x = x / np.sqrt(np.average(np.square(x)))
    return x


def synthesize_green(len_s, f_hz):
    a = generate_adsr_envelope(len_s, 0.05 * len_s, 0, 1, 0.2 * len_s)
    x = a * (generate_fm_wave(len_s, f_hz, f_hz, 0.5)
             + 0.33 * generate_fm_wave(len_s, f_hz, 2 * f_hz, 0.2))
    x = x / np.sqrt(np.average(np.square(x)))
    return x


def synthesize_red(len_s, f_hz):
    a = generate_adsr_envelope(len_s,
                               0.09 * len_s, 0.01 * len_s, 0.75, 0.5 * len_s)
    e = generate_adsr_envelope(len_s, 0.1 * len_s, 0, 1, 0.1 * len_s)
    x = a * (generate_fm_wave(len_s, f_hz, f_hz, 6.2 + 4 * e)
             + 0.33 * generate_fm_wave(len_s, f_hz, f_hz, 2.8 * e))
    x = x / np.sqrt(np.average(np.square(x)))
    return x


def read_wav(file_name):
    x = wavfile.read(AUDIO_DIR + file_name)[1]

    if x.dtype == np.uint8:
        x = (x - 2 ** 7) / (2 ** 7 - 1)
    elif x.dtype == np.int16:
        x = x / (2 ** 15 - 1)
    elif x.dtype == np.int32:
        x = x / (2 ** 31 - 1)
    # input is normalized to [-1, 1].

    return x


def write_wav(file_name, x):
    wavfile.write(AUDIO_DIR + file_name, FS_HZ, x.astype(np.float32))


def initialize_audio_player():
    pygame.mixer.init()


def play_audio(file_name):
    audio = pygame.mixer.Sound(AUDIO_DIR + file_name)
    audio.play()
