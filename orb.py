import numpy as np
import cv2
from matplotlib import pyplot as plt
import math

MIN_MATCH_COUNT = 50 # TODO SET THIS HIGHER?

# note img1 and img2 swapped so trainImage and queryImage would
# be the same as in the tutorial.
img1 = cv2.imread('2fingers.jpg',0) # queryImage
img2 = cv2.imread('1fingers.jpg',0) # trainImage
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

h, w = (int(img1.shape[0]), int(img1.shape[1]))
print("height, width", h, w)

# Draw first 10 matches
img3 = cv2.drawMatches(img1, kp1, img2, kp2, None, None, flags=2) # When you want to draw the infinite connector lines, try the first None = matches[:300]
# TODO look into allowing for more matches,
# TODO show less match cancellatoins (left/right_count)
# TODO: change sizes by counting proximity aka clustering

# counts how many matches are not transferred over
# e.g. left_count[i][j] having 3 means three matches
left_count = [[0 for i in range(h//100+1)] for j in range(w//100+1)] # +1 bc why not
right_count = [[0 for i in range(h//100+1)] for j in range(w//100+1)]

# TODO RN!!! DON'T DRAW CIRCLES FOR MATCHES!!! ONLY DRAW CIRCLES FOR NO MATCHES!!

left_matches = set()
right_matches = set()
for match in matches:  # It seems matches is capped at 500
    left_matches.add(kp1[match.trainIdx].pt[0])
    right_matches.add(kp2[match.queryIdx].pt[0])

for item in kp1:
    cv2.circle(img3, tuple(map(int, item.pt)), 60, (180, 180, 100), 5)

for item in kp2:
    cv2.circle(img3, (int(item.pt[0]+w), int(item.pt[1])), 60, (240, 240, 200), 5)

print("kp1 len", len(kp1))
for ob in kp1:
    pt = (int(ob.pt[0]), int(ob.pt[1]))
    if pt not in left_matches:
        left_count[pt[0]//100][pt[1]//100] += 1
for ob in kp2:
    pt = (int(ob.pt[0]), int(ob.pt[1]))
    if pt not in right_matches:
        right_count[(pt[0])//100][(pt[1])//100] += 1


# GHETTO CODE
''' TODO These would be the blues. OR NOT
for match in matches[:100]:
    pt1 = (int(kp1[match.queryIdx].pt[0]), int(kp1[match.queryIdx].pt[1]))
    temp_pt2 = (int(kp2[match.trainIdx].pt[0]), int(kp2[match.trainIdx].pt[1]))
    pt2 = (temp_pt2[0], temp_pt2[0])
    ghetto_count[pt1[0]//100][pt1[1]//100] += 1
    ghetto_count[pt2[0]//100][pt2[1]//100] += 1
'''
'''
    if dist(pt1, pt2) > 40: # WTF IS THIS <--- # TODO change this from constant to variable based on size
        cv2.circle(img3, pt1, 200, (240,10,10), 5)
        cv2.circle(img3, pt2, 200, (240,10,10), 5)
'''

COUNT_THRESHOLD = 15

for r in range(len(left_count)):
    for c in range(len(left_count[r])):
        if (left_count[r][c] > COUNT_THRESHOLD):
            cv2.circle(img3, (r*100+50, c*100+50), left_count[r][c]*15, (40, 40, 240), (left_count[r][c]+1)//2) #only adding 50 means at BOTTOM RIGHT corner the +50 pushes out of screen if last box is 20x20 say for 1020x1020 e.g..
            cv2.circle(img3, (r*100+50+w, c*100+50), left_count[r][c]*15, (240, 10, 10), (left_count[r][c]+1)//2)

for r in range(len(right_count)):
    for c in range(len(right_count[r])):
        if (right_count[r][c] > COUNT_THRESHOLD):
            cv2.circle(img3, (r*100+50, c*100+50), right_count[r][c]*15, (40, 40, 240), (right_count[r][c]+1)//2) #only adding 50 means at BOTTOM RIGHT corner the +50 pushes out of screen if last box is 20x20 say for 1020x1020 e.g..
            cv2.circle(img3, (r*100+50+w, c*100+50), right_count[r][c]*15, (10, 240, 10), (right_count[r][c]+1)//2)

#TODO: frontend add options for which colors to allow

#These two lines help to tell placements to base other judgments on.
#cv2.circle(img3, (0, 500), 100, (10, 240, 80), 20)
#cv2.circle(img3, (w, h), 100, (10, 240, 80), 20)
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
