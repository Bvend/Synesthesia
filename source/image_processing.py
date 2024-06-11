# module dedicated to pre-processing input photos so that they're as close as
# possible to the user's intended drawings.
# for the translation of images to note matrices and audio, check composer.


import cv2 as cv
import numpy as np


IMG_DIR = '../resources/images/' # directory for image input/output.


def load_image(file_name):
    img = cv.imread(IMG_DIR + file_name, cv.IMREAD_COLOR)
    return img


def binarize_image(img, debug = False):
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray =  cv.GaussianBlur(gray_img,(5,5),0)
    bin_img = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv.THRESH_BINARY, 11, 5)
    ret, bin_img_borda= cv.threshold(gray,80,255,cv.THRESH_BINARY)

    ni, nj = bin_img_borda.shape
    nd = min(ni, nj)

    miniI = 0
    miniJ = 0
    maxI = nj
    maxJ = nj
    f = False
    for d in range(nd):
        for x in range(d+1):
            i = x
            j = d-x
            if bin_img_borda[i, j] == 255:
                miniJ = max(miniJ, j)
                miniI = max(miniI, i)
                f = True
                break
        if f:
            break


    f = False
    for d in range(nd):
        for x in range(d+1):
            i = ni-1-x
            j = d-x
            if bin_img_borda[i, j] == 255:
                miniJ = max(miniJ, j)
                maxI = min(maxI, i)
                f = True
                break
        if f:
            break

    f = False
    for d in range(nd):
        for x in range(d+1):
            i = x
            j = nj-1-d+x
            if bin_img_borda[i, j] == 255:
                maxJ = min(maxJ, j)
                miniI = max(miniI, i)
                f = True
                break
        if f:
            break

    f = False
    for d in range(nd):
        for x in range(d+1):
            i = ni-1-x
            j = nj-1-d+x
            if bin_img_borda[i, j] == 255:
                maxJ = min(maxJ, j)
                maxI = min(maxI, i)
                f = True
                break
        if f:
            break

    delta = 5
    miniI += delta
    miniJ += delta
    maxI -= delta
    maxJ -= delta
    pts1 = np.float32([[miniI, miniJ], [maxI, miniJ], [miniI, maxJ], [maxI, maxJ]])
    '''cv.circle(img, (miniJ, miniI), 2, (0, 255, 0), -1)
    cv.circle(img, (miniJ, maxI), 2, (0, 255, 0), -1)
    cv.circle(img, (maxJ, miniI), 2, (0, 255, 0), -1)
    cv.circle(img, (maxJ, maxI), 2, (0, 255, 0), -1)'''
    pts2 = np.float32([[0, 0], [0, ni - 1], [nj - 1, nj - 1], [ni - 1, nj - 1]])
    M = cv.getPerspectiveTransform(pts1, pts2)
    #img_cortada = cv.warpPerspective(bin_img, M, (nj, ni))
    bin_img = bin_img[miniI:maxI, miniJ:maxJ]
    img = img[miniI:maxI, miniJ:maxJ]

    if debug == True:
        cv.imshow('binarized', bin_img)
        cv.imwrite(IMG_DIR + 'test_binarized.jpg', bin_img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    return img, bin_img


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
        cv.imwrite(IMG_DIR + 'test_colored.jpg', colored_img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    return colored_img
