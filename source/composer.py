# module dedicated to translating pre-processed images to audio tracks, through
# intermediate note matrices.
# for the pre-processing of images, check image_processing;
# for the synthetization and output of audio, check synthesizer.


from synthesizer import FS_HZ, amplify_signal, \
                        synthesize_blue, synthesize_green, synthesize_red

import numpy as np


NUM_ROWS = 40 # number of rows, i.e. frequencies, of note matrices. 40 is three
              # octaves less than the 88 in most modern pianos.

NUM_COLS = 128 # number of columns, i.e. time intervals, of note matrices.

F = 440 * (2 ** ((np.arange(NUM_ROWS) - 24) / 12))
# note frequencies array. A4 = 440 Hz, a standard tuning pitch, is taken as the
# reference frequency. indexing it by 24 on an array of 40 sets the range to
# A2-C6.

COL_S = 60 / (120 * 4) # time length assigned to each matrix column. the values
                       # in the expression are chosen so that each beat in a
                       # 120 bpm pace is assigned to four columns.

LEVEL_REF_DB = 85 # maximum sound level expected on the device. 85 dB is
                  # assumed, as it is the limit for safe long-term exposure;
                  # however, the higher this value, the greater the attenuation
                  # performed on the output, and thus, the safer.

GAIN_DB = 60 - LEVEL_REF_DB # output gain. 60 dB is the desired sound level, a
                            # moderate, conversational one.


def get_notes_from_image(bin_img, color_img, debug = False):
    # split the image into sections:
    h, w = bin_img.shape
    i_split = np.round(
                  np.linspace(0, h, num = NUM_ROWS, endpoint = False)[1 :]
              ).astype(int)
    j_split = np.round(
                  np.linspace(0, w, num = NUM_COLS, endpoint = False)[1 :]
              ).astype(int)
    bin_sections = [np.split(row_split, j_split, axis = 1)
                    for row_split in np.split(bin_img, i_split, axis = 0)]
    color_sections = [np.split(row_split, j_split, axis = 1)
                      for row_split in np.split(color_img, i_split, axis = 0)]

    # count color occurrences in each section:
    where = np.nonzero # function alias for readability.
    cnt_color = np.array(
        [[np.sum(color_section[where(bin_section == 0)] == 255, axis = 0)
          for bin_section, color_section in zip(bin_row, color_row)]
         for bin_row, color_row in zip(bin_sections, color_sections)])
    cnt_b, cnt_g, cnt_r = np.moveaxis(cnt_color, 2, 0)

    cnt_tot = cnt_b + cnt_g + cnt_r
    size_section = np.array([[bin_section.size
                              for bin_section in row]
                             for row in bin_sections])
    is_colored = cnt_tot >= size_section / 8
    color_is_b = is_colored & (cnt_b > cnt_g) & (cnt_b > cnt_r)
    color_is_g = is_colored & ~color_is_b & (cnt_g > cnt_r)
    color_is_r = is_colored & ~color_is_b & ~color_is_g
    notes = np.zeros((NUM_ROWS, NUM_COLS))
    notes[where(color_is_b)] = 1
    notes[where(color_is_g)] = 2
    notes[where(color_is_r)] = 3

    if debug == True:
        from plotter import plot_note_matrix
        plot_note_matrix('test_notes.jpg', notes)

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
                        note = synthesize_blue(
                                 note_len * COL_S, F[NUM_ROWS - 1 - i])
                    elif note_timbre == 2:
                        note = synthesize_green(
                                 note_len * COL_S, F[NUM_ROWS - 1 - i])
                    else:
                        note = synthesize_red(
                                 note_len * COL_S, F[NUM_ROWS - 1 - i])
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


def get_audio_from_image(bin_img, color_img, debug = False):
    notes = get_notes_from_image(bin_img, color_img, debug)
    audio = get_audio_from_notes(notes)
    return audio
