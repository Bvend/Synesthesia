import cv2 as cv
img = cv.imread('Synesthesia/source/img1.bmp', cv.IMREAD_COLOR)
gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
bin_img = cv.adaptiveThreshold(gray_img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,5)
cv.imshow('binarizada', bin_img)
print(bin_img.shape)
cv.waitKey(0)
cv.destroyAllWindows()
