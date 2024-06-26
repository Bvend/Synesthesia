# test module dedicated to plotting note matrices and one-dimensional signals.


from image_processing import IMG_DIR
from synthesizer import FS_HZ
from composer import NUM_ROWS, NUM_COLS, LEVEL_REF_DB

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


M_RATIO = 0.05 # ratio of the plot's margins to their axis' limits.


def plot_note_matrix(file_name, notes):
    plt.matshow(notes, cmap = ListedColormap([[1, 1, 1],
                                              [0, 0, 1], [0, 1, 0], [1, 0, 0]]))
    plt.xticks(np.arange(NUM_COLS + 1) - 0.5, minor = True)
    plt.xticks(np.arange(0, NUM_COLS + 1, 8) - 0.5,
               labels = np.arange(0, NUM_COLS + 1, 8))
    plt.yticks(np.arange(NUM_ROWS + 1) - 0.5, minor = True)
    plt.yticks(np.arange(4, NUM_ROWS + 1, 12) - 0.5,
               labels = np.arange(4, NUM_ROWS + 1, 12))
    plt.title('Note matrix')
    plt.grid(visible = True, which = 'minor', alpha = 0.25)
    plt.grid(visible = True, which = 'major', alpha = 0.5)
    plt.savefig(IMG_DIR + file_name)
    plt.clf()


def plot_waveform(file_name, x, in_db = False, l_s = 0, r_s = np.inf):
    t = np.arange(len(x)) / FS_HZ
    if in_db:
        x = np.where(x != 0, 20 * np.log10(abs(x), where = (x != 0)), -np.inf)
        # level_db = 20 * log10(amplitude / amplitude_ref);
        # see synthesizer.amplify_signal for details.

    if r_s == np.inf:
        r_s = len(x) / FS_HZ
    m_s = M_RATIO * (r_s - l_s) # x axis' margins.

    plt.plot(t, x)
    plt.xlabel('Time [s]')
    plt.xlim(l_s - m_s, r_s + m_s)
    plt.ylabel('Amplitude' + (' [dB]' if in_db else ''))
    if in_db:
        plt.ylim(-(1 + M_RATIO) * LEVEL_REF_DB, M_RATIO * LEVEL_REF_DB)
    plt.title('Waveform')
    plt.grid(visible = True)
    plt.savefig(IMG_DIR + file_name)
    plt.clf()


def plot_frequency(file_name, x, in_db = False, l_hz = 0, r_hz = FS_HZ / 2):
    f = np.linspace(0, FS_HZ, num = len(x), endpoint = False)
    x = abs(np.fft.fft(x, norm = 'forward'))
    if in_db:
        x = np.where(x != 0, 20 * np.log10(x, where = (x != 0)), -np.inf)

    m_hz = M_RATIO * (r_hz - l_hz)

    plt.plot(f, x)
    plt.xlabel('Frequency [Hz]')
    plt.xlim(l_hz - m_hz, r_hz + m_hz)
    plt.ylabel('Amplitude' + (' [dB]' if in_db else ''))
    if in_db:
        plt.ylim(-(1 + M_RATIO) * LEVEL_REF_DB, M_RATIO * LEVEL_REF_DB)
    plt.title('Frequency')
    plt.grid(visible = True)
    plt.savefig(IMG_DIR + file_name)
    plt.clf()


def plot_phase(file_name, x, l_hz = 0, r_hz = FS_HZ / 2):
    f = np.linspace(0, FS_HZ, num = len(x), endpoint = False)
    x = np.fft.fft(x, norm = 'forward')
    x = np.where(abs(x) > 10 ** (-LEVEL_REF_DB / 20), np.angle(x), 0)
    # prevents negligible frequencies from polluting the plot.
    # amplitude = amplitude_ref * 10 ^ (level_db / 20);
    # see synthesizer.amplify_signal for details.

    m_hz = M_RATIO * (r_hz - l_hz)

    plt.plot(f, x)
    plt.xlabel('Frequency [Hz]')
    plt.xlim(l_hz - m_hz, r_hz + m_hz)
    plt.ylabel('Phase [rad]')
    plt.ylim(-(1 + 2 * M_RATIO) * np.pi, (1 + 2 * M_RATIO) * np.pi)
    plt.title('Phase')
    plt.grid(visible = True)
    plt.savefig(IMG_DIR + file_name)
    plt.clf()
