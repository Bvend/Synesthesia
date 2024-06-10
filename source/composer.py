# module dedicated to translating pre-processed images to audio tracks, through
# intermediate note matrices.
# for the pre-processing of images, check image_processing;
# for the synthetization and output of audio, check synthesizer.


from synthesizer import *

import numpy as np


NUM_ROWS = 40 # number of rows, i.e. frequencies, of note matrices. 76 is one
              # less octave than the 88 in most modern pianos.

NUM_COLS = 128 # number of columns, i.e. time intervals, of note matrices.

F = 440 * (2 ** ((np.arange(NUM_ROWS) - 24) / 12))
# note frequencies array. A4 = 440 Hz, a standard tuning pitch, is taken as the
# reference frequency. indexing it by 48 on an array of 76 sets the range to
# A0-C7.

COL_S = 60 / (120 * 4) # time length assigned to each matrix column. the values
                       # in the expression are chosen so that each beat in a
                       # 120 bpm pace is assigned to four columns.

LEVEL_REF_DB = 85 # maximum sound level expected on the device. 85 dB is
                  # assumed, as it is the limit for safe long-term exposure;
                  # however, the higher this value, the greater the attenuation
                  # performed on the output, and thus, the safer.

GAIN_DB = 60 - LEVEL_REF_DB # output gain. 60 dB is the desired sound level, a
                            # moderate, conversational one.


def get_notes_from_image(bin_img, colored_img, debug = False):
    h_img, w_img = bin_img.shape

    notes = np.zeros((NUM_ROWS, NUM_COLS))
    for i in range(NUM_ROWS):
        for j in range(NUM_COLS):
            cnt_b = 0
            cnt_g = 0
            cnt_r = 0
            for y in range(int(np.round(i * h_img / NUM_ROWS)),
                           int(np.round((i + 1) * h_img / NUM_ROWS))):
                for x in range(int(np.round(j * w_img / NUM_COLS)),
                               int(np.round((j + 1) * w_img / NUM_COLS))):
                    if bin_img[y, x] == 255:
                        continue
                    if colored_img[y, x, 0] == 255:
                        cnt_b += 1
                    elif colored_img[y, x, 1] == 255:
                        cnt_g += 1
                    elif colored_img[y, x, 2] == 255:
                        cnt_r += 1
            if cnt_b + cnt_g + cnt_r > (h_img/40) * (w_img/128) / 3:
                if cnt_b > cnt_g and cnt_b > cnt_r:
                    notes[i, j] = 1 # blue.
                elif cnt_g > cnt_r:
                    notes[i, j] = 2 # green.
                else:
                    notes[i, j] = 3 # red.

    if debug == True:
        from plotter import plot_note_matrix
        plot_note_matrix('../resources/images/test_notes.png', notes)

    return notes


def get_audio_from_notes(notes):
    audio = np.zeros(int(np.round(NUM_COLS * COL_S * FS_HZ)))
    for i in range(NUM_ROWS):
        note_begin = 0 # first column of the current note.
        note_len = 1 # length in columns of the current note.
        note_timbre = notes[i, 0] # timbre of the current note.
        for j in range(1, NUM_COLS + 1):
            if j < NUM_COLS and notes[i, j] == notes[i, j - 1]:
                note_len += 1
            else:
                if note_len > 0 and note_timbre != 0:
                    if note_timbre == 1:
                        note = synthetize_blue(# generate_square_wave(
                                 note_len * COL_S, F[NUM_ROWS - 1 - i]) # blue.
                    elif note_timbre == 2:
                        note = synthetize_green(# generate_sine_wave(
                                 note_len * COL_S, F[NUM_ROWS - 1 - i]) # green.
                    else:
                        note = synthetize_red(# generate_sawtooth_wave(
                                 note_len * COL_S, F[NUM_ROWS - 1 - i]) # red.
                    begin_sample = int(np.round(note_begin * COL_S * FS_HZ))
                    len_samples = int(np.round(note_len * COL_S * FS_HZ))
                    end_sample = begin_sample + len_samples
                    audio[begin_sample : end_sample] += note[0 : len_samples]
                if j < NUM_COLS:
                    note_begin = j
                    note_len = 1
                    note_timbre = notes[i, j]
    audio = amplify_signal(audio, GAIN_DB) # since the gain is negative,
                                           # actually attenuates the output.
    return audio
