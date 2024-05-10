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
        cv.imwrite('binarized.bmp', bin_img)
        cv.waitKey(0)
        #cv.destroyAllWindows()

    return bin_img


def classify_rgb(img, bin_img, debug = False):
    img_colored = img.copy()

    for i, row in enumerate(img):
        for j, pixel in enumerate(img):
            if bin_img[i][j] == 255:
                continue
            dr = (img[i][j][0] - 255)**2 + img[i][j][1]**2 + img[i][j][2]**2
            dg = img[i][j][0]**2 + (img[i][j][1] - 255)**2 + img[i][j][2]**2
            db = img[i][j][0]**2 + img[i][j][1]**2 + (img[i][j][2] - 255)**2
            if dr < dg and dr < db:
                img_colored[i][j] = [255, 0, 0]
            elif dg < dr and dg < db:
                img_colored[i][j] = [0, 255, 0]
            else:
                img_colored[i][j] = [0, 0, 255]

    cv.imshow('colored', img_colored)
    cv.imwrite('colored.bmp', img_colored)
    cv.waitKey(0)
    cv.destroyAllWindows()
    return img_colored


# Altura de img deve ser multiplo de num_notes
# Comprimento de img deve ser multiplo de note_duration
def get_notes_from_image(img, color_img, num_notes, note_duration):
    img = np.asarray(img)
    h, w = img.shape
    row_h = h // num_notes
    num_interv = w // note_duration
    notes = np.zeros((num_notes, num_interv))
    for i in range(num_notes):
        for j in range(num_interv):
            sum = 0
            red = 0
            green = 0
            blue = 0
            for y in range(row_h):
                for x in range(note_duration):
                    sum += img[i * row_h + y, j * note_duration + x] == 0
                    if color_img[i * row_h + y][j * note_duration + x][0] == 255:
                        red += 1
                    elif color_img[i * row_h + y][j * note_duration + x][1] == 255:
                        green += 1
                    else:
                        blue += 1
            if sum > 0:
                tim = 3
                if red > green and red > blue:
                    tim = 1
                elif green > red and green > blue:
                    tim = 2
                notes[i, j] = tim

    return notes


# Funcao temporaria
def generate_test_image():
    img = np.zeros((216,300,3), np.uint8)
    for y in range(len(img)):
        for x in range(len(img[0])):
            img[y,x] = [255,255,255]
    #cv.rectangle(img,(30,100),(99,98),(255,0,0),-1)
    cv.imwrite('/home/bernardo/codes/Synesthesia/source/test.bmp', img)
