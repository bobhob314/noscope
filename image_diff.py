# Note that this is just a test for totally stable images.
# Written by Max Li.

from skimage.measure import compare_ssim
import argparse
import imutils
import cv2

#construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--first", required=True,
    help="first input image")
ap.add_argument("-s", "--second", required=True,
    help="second")
args = vars(ap.parse_args())

imageA = cv2.imread(args["first"])
imageB = cv2.imread(args["second"])

grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

# compute Structural Similarity Index (SSIM).
(score, diff) = compare_ssim(grayA, grayB, full=True)
diff = (diff * 255).astype("uint8")
print("SSIM: {}".format(score))

# threshold difference image, find contours to obtain regions of difference
thresh = cv2.threshold(diff, 0, 255,
    cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

# loop over the contours
for c in cnts:
    (x, y, w, h) = cv2.boundingRect(c)
    cv2.rectangle(imageA, (x, y), (x+w, y+h), (0, 0, 255), 2)
    cv2.rectangle(imageB, (x, y), (x+w, y+h), (0, 0, 255), 2)

#cv2.imshow("Original", imageA)
#cv2.imshow("Modified", imageB)
#cv2.imshow("Diff", diff)
#cv2.imshow("thresh", thresh)
#cv2.waitKey(0)

cv2.imwrite('1rect.jpg', imageA)
cv2.imwrite('2rect.jpg', imageB)
cv2.imwrite('diff.jpg', diff)
cv2.imwrite('thresh.jpg', thresh)

# Just testing that the files actually are grayed properly.
#cv2.imwrite('1gray.jpg', grayA)
#cv2.imwrite('2gray.jpg', grayB)
