# module dedicated to pre-processing input photos so that they're as close as
# possible to the user's intended drawings.
# for the translation of images to note matrices and audio, check composer.


import cv2 as cv


def load_image(img_path):
    img = cv.imread(img_path, cv.IMREAD_COLOR)
    return img


def binarize_image(img, debug = False):
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    bin_img = cv.adaptiveThreshold(gray_img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv.THRESH_BINARY, 11, 5)

    if debug == True:
        cv.imshow('binarized', bin_img)
        cv.imwrite('../resources/images/test_binarized.bmp', bin_img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    return bin_img


def classify_rgb(img, bin_img, debug = False):
    colored_img = img.copy()

    for i, row in enumerate(img):
        for j, (b, g, r) in enumerate(row):
            if bin_img[i, j] == 255:
                continue
            db = (b - 255) ** 2 + g ** 2 + r ** 2 # squared euclidean distances.
            dg = b ** 2 + (g - 255) ** 2 + r ** 2
            dr = b ** 2 + g ** 2 + (r - 255) ** 2
            if db < dg and db < dr:
                colored_img[i, j] = [255, 0, 0] # blue.
            elif dg < dr:
                colored_img[i, j] = [0, 255, 0] # green.
            else:
                colored_img[i, j] = [0, 0, 255] # red.

    if debug == True:
        cv.imshow('colored', colored_img)
        cv.imwrite('../resources/images/test_colored.bmp', colored_img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    return colored_img
