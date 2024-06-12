# module dedicated to pre-processing input photos so that they're as close as
# possible to the user's intended drawings.
# for the translation of images to note matrices and audio, check composer.


import cv2 as cv
import numpy as np


IMG_DIR = '../resources/images/' # directory for image input/output.

B = np.array([255, 0, 0]) # colors.
G = np.array([0, 255, 0])
R = np.array([0, 0, 255])


def load_image(file_name):
    img = cv.imread(IMG_DIR + file_name, cv.IMREAD_COLOR)
    return img


def find_crop_points(img):
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur_img = cv.GaussianBlur(gray_img, (5, 5), 0)
    ret, bin_img = cv.threshold(blur_img, 80, 255, cv.THRESH_BINARY)

    h, w = bin_img.shape
    searches = [((k, d - k)
                 for d in range(h + w - 1) for k in range(h)
                 if d - k >= 0 and d - k < w),
                ((k, (w - 1) - (d - k))
                 for d in range(h + w - 1) for k in range(h)
                 if (w - 1) - (d - k) >= 0 and (w - 1) - (d - k) < w),
                (((h - 1) - k, d - k)
                 for d in range(h + w - 1) for k in range(h)
                 if d - k >= 0 and d - k < w),
                (((h - 1) - k, (w - 1) - (d - k))
                 for d in range(h + w - 1) for k in range(h)
                 if (w - 1) - (d - k) >= 0 and (w - 1) - (d - k) < w)]
    # each search iterates through the (i, j) pairs of a breadth-first traversal
    # starting from a corner of the image.

    pts = np.float32([next((j, i)
                           for i, j in search
                           if bin_img[i, j] == 255)
                      for search in searches])
    # white pixels closest to the corners.

    lx = max(pts[0, 0], pts[2, 0])
    rx = min(pts[1, 0], pts[3, 0])
    ly = max(pts[0, 1], pts[1, 1])
    ry = min(pts[2, 1], pts[3, 1])
    pts = np.float32([[lx, ly], [rx, ly], [lx, ry], [rx, ry]])
    # crop to a rectangle inside the quadrangle to further avoid the drawing's
    # edges.

    return pts


def crop_image(img, crop_pts, debug = False):
    h, w = img.shape[0 : 2]
    corner_pts = np.float32([(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)])
    m = cv.getPerspectiveTransform(crop_pts, corner_pts)
    crop_img = cv.warpPerspective(img, m, (w, h))

    if debug == True:
        cv.imshow('cropped', crop_img)
        cv.imwrite(IMG_DIR + 'test_cropped.jpg', crop_img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    return crop_img


def binarize_image(img, debug = False):
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur_img = cv.GaussianBlur(gray_img, (5, 5), 0)
    bin_img = cv.adaptiveThreshold(blur_img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv.THRESH_BINARY, 11, 5)

    if debug == True:
        cv.imshow('binarized', bin_img)
        cv.imwrite(IMG_DIR + 'test_binarized.jpg', bin_img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    return bin_img


def classify_rgb(img, bin_img, debug = False):
    where = np.nonzero # function alias for readability.

    colors = np.copy(img[where(bin_img == 0)])
    db = np.linalg.norm(colors - B, axis = 1) # euclidean distances.
    dg = np.linalg.norm(colors - G, axis = 1)
    dr = np.linalg.norm(colors - R, axis = 1)
    color_is_b = (db < dg) & (db < dr) # map to the closest color.
    color_is_g = ~color_is_b & (dg < dr)
    color_is_r = ~color_is_b & ~color_is_g
    colors[where(color_is_b)] = B
    colors[where(color_is_g)] = G
    colors[where(color_is_r)] = R
    color_img = np.copy(img)
    color_img[where(bin_img == 0)] = colors

    if debug == True:
        cv.imshow('colored', color_img)
        cv.imwrite(IMG_DIR + 'test_colored.jpg', color_img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    return color_img


def pre_process_image(img, debug = False):
    crop_pts = find_crop_points(img)
    crop_img = crop_image(img, crop_pts, debug)
    bin_img = binarize_image(crop_img, debug)
    color_img = classify_rgb(crop_img, bin_img, debug)
    return bin_img, color_img
