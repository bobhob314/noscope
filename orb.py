import numpy as np
import cv2
from matplotlib import pyplot as plt
import math
# note img1 and img2 swapped so trainImage and queryImage would
# be the same as in the tutorial.
img1 = cv2.imread('2.jpg',0) # queryImage
img2 = cv2.imread('1.jpg',0) # trainImage
# Initiate ORB detector
orb = cv2.ORB_create()
# find the keypoints with ORB compute the descriptors with ORB
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

# create BFMatcher
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Match descsriptors
matches = bf.match(des1, des2)

# Sort them in the order of their distance
matches = sorted(matches, key = lambda x:x.distance)

def dist(p0, p1):
    return ((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)**(1/2)

h, w = img1.shape[:2]
print("width, height", w, h)

# Draw first 10 matches
img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches[:300], None, flags=2)

# TODO: change sizes by counting proximity aka clustering
ghetto_count = [[0 for i in range(int(math.ceil(img3.shape[1])))] for j in range(int(math.ceil(img3.shape[0])))] # TODO TODO TODO

# TODO RN!!! DON'T DRAW CIRCLES FOR MATCHES!!! ONLY DRAW CIRCLES FOR NO MATCHES!!

left_matches = set()
right_matches = set()
for match in matches[:400]:
    left_matches.add(kp1[match.queryIdx].pt[0])
    right_matches.add(kp2[match.queryIdx].pt[0])

print("kp1 len", len(kp1))
for ob in kp1:
    pt = (int(ob.pt[0]), int(ob.pt[1]))
    if pt not in left_matches:
        ghetto_count[pt[0]//100][pt[1]//100] += 1
for ob in kp2:
    pt = (int(ob.pt[0]), int(ob.pt[1]))
    if pt not in right_matches:
        ghetto_count[(pt[0]+w)//100][(pt[1])//100] += 1


# GHETTO CODE
'''
for match in matches[:100]:
    pt1 = (int(kp1[match.queryIdx].pt[0]), int(kp1[match.queryIdx].pt[1]))
    temp_pt2 = (int(kp2[match.trainIdx].pt[0]), int(kp2[match.trainIdx].pt[1]))
    pt2 = (temp_pt2[0]+w, temp_pt2[0])
    ghetto_count[pt1[0]//100][pt1[1]//100] += 1
    ghetto_count[pt2[0]//100][pt2[1]//100] += 1
'''
'''
    if dist(pt1, pt2) > 40: # WTF IS THIS <--- # TODO change this from constant to variable based on size
        cv2.circle(img3, pt1, 200, (240,10,10), 5)
        cv2.circle(img3, pt2, 200, (240,10,10), 5)
'''

for r in range(len(ghetto_count)):
    for c in range(len(ghetto_count[r])):
        if (ghetto_count[r][c]):
            if (r+1)*100
            cv2.circle(img3, (r*100+50, c*100+50), ghetto_count[r][c]*20, (240, 10, 10), ghetto_count[r][c]) #only adding 50 means at BOTTOM RIGHT corner the +50 pushes out of screen if last box is 20x20 say for 1020x1020 e.g..
            cv2.circle(img3, (r*100+50+w, c*100+50), ghetto_count[r][c]*20, (240, 10, 10), ghetto_count[r][c])
            cv2.circle(img3, (r*100+50-w, c*100+50), ghetto_count[r][c]*20, (240, 10, 10), ghetto_count[r][c])
cv2.circle(img3, (0, 500), 100, (10, 240, 80), 20)
cv2.circle(img3, (w, h), 100, (10, 240, 80), 20)
# could use line sweep to make faster.

print(kp1[0].pt)
print(matches[0].distance)
print(matches[0].trainIdx)
print(matches[0].queryIdx)
print(matches[0].imgIdx)

img4 = cv2.imread('2.jpg',0) # queryImage
img5 = cv2.imread('1.jpg',0) # trainImage

# TODO LET THESE HAVE COLOR. harder than i thought actually.

plt.imshow(img3), plt.show()
