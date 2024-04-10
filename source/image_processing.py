import numpy as np
import cv2 as cv


# def take_photo():
#    photo = cv.imread('/home/bernardo/codes/Synesthesia/source/default.bmp', cv.IMREAD_COLOR)
#    return photo


def load_image(img_path):
    img = cv.imread(img_path, cv.IMREAD_COLOR)
    return img


def binarize_image(img, debug = False):
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    bin_img = cv.adaptiveThreshold(gray_img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 5)

    if debug == True:
        cv.imshow('binarized', bin_img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    return bin_img


# Altura de img deve ser multiplo de num_notes
# Comprimento de img deve ser multiplo de note_duration
def get_notes_from_image(img, num_notes, note_duration):
    img = np.asarray(img)
    h, w = img.shape
    row_h = h // num_notes
    num_interv = w // note_duration
    notes = np.zeros((num_notes, num_interv))
    for i in range(num_notes):
        for j in range(num_interv):
            sum = 0
            for y in range(row_h):
                for x in range(note_duration):
                    sum += img[i * row_h + y][j * note_duration + x] == 0
            notes[i][j] = sum > 4
    return notes


# Funcao temporaria
def generate_test_image():
    img = np.zeros((180,300,3), np.uint8) # shape(h, l, d)
    for y in range(len(img)):
        for x in range(len(img[0])):
            img[y,x] = [255,255,255]

    cv.rectangle(img,(0,177),(300,179),(255,0,0),-1)
