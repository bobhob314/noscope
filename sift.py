import cv2
import numpy as np
from matplotlib import pyplot as plt
import os, sys

fn1 = sys.argv[1]
fn2 = sys.argv[2]
clr = sys.argv[3]
print(str(fn1), str(fn2))

#TODO what if no arguments given or not proper ones

# TODO AUTOMATE THRESHOLDS!!!! AND MULTIPLICATIVE FACTORS!!
sift = cv2.xfeatures2d.SIFT_create()

#img1
img1 = cv2.imread(fn1)
gray1= cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
kp1, des1 = sift.detectAndCompute(gray1,None)
#img1=cv2.drawKeypoints(gray1,kp1,img1)
#cv2.imwrite('1sift_keypoints.jpg',img1)
#img1=cv2.drawKeypoints(gray1,kp1,img1,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
#cv2.imwrite('1sift_keypoints2.jpg',img1)

#img2
img2 = cv2.imread(fn2)
gray2= cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
kp2, des2 = sift.detectAndCompute(gray2,None)
#img2=cv2.drawKeypoints(gray2,kp2,img2)
#cv2.imwrite('2sift_keypoints.jpg',img2)
#img2=cv2.drawKeypoints(gray2,kp2,img2,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
#cv2.imwrite('2sift_keypoints2.jpg',img2) # kinda repeated. here and above.

print(len(kp1), len(kp2))
average_features = (len(kp1)+len(kp2))//2
COUNT_THRESHOLD = average_features//300 # pretty sure should be exponential but hey
RADIUS_DIVISOR = average_features//2
STROKE_DIVISOR = average_features*10

#matching
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)
flann = cv2.FlannBasedMatcher(index_params, search_params)
all_matches = flann.knnMatch(des1,des2,k=2)

img3 = cv2.drawMatches(img1, kp1, img2, kp2, None, None, flags=2) # When you want to draw the infinite connector lines, try the first None = matches[:300]

# store all the good matches as per Lowe's ratio test.
matches = []
for m,n in all_matches:
    if m.distance < 0.7*n.distance:
        matches.append(m)

# Sort them in the order of their distance
matches = sorted(matches, key = lambda x:x.distance)

h, w = (int(img1.shape[0]), int(img1.shape[1]))


left_count = [[0 for i in range(h//100+1)] for j in range(w//100+1)] # +1 bc why not
right_count = [[0 for i in range(h//100+1)] for j in range(w//100+1)]

DELTA_THRESHOLD = 500 # only show matches if above delta (movement) THRESHOLDS
# show all things in kp1 that aren't matched, kp2 that aren't matched.

# left matches, right matches
left_matches = dict()
right_matches = dict()
print(len(kp1), len(kp2))

def dist(p0, p1):
    return ((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)**(1/2)

for match in matches:  # It seems matches is capped at 500
    # srsly dunno why but gotta switch them


    #if (dist(kp1[match.queryIdx].pt, kp2[match.trainIdx].pt)> DELTA_THRESHOLD): # !! technically should check, add all here. later if not in add to not in. THEN if distance hi, add.
    #print(kp1[match.queryIdx].pt, kp2[match.trainIdx].pt, dist(kp1[match.queryIdx].pt, kp2[match.trainIdx].pt))
    left_matches[kp1[match.queryIdx].pt] = match
    right_matches[kp2[match.trainIdx].pt] = match

#for item in kp1:
#    cv2.circle(img3, tuple(map(int, item.pt)), 10, (180, 180, 100), 1)

#for item in kp2:
#    cv2.circle(img3, (int(item.pt[0]+w), int(item.pt[1])), 10, (240, 240, 200), 1)

print("kp1 len", len(kp1))
for ob in kp1:
    pt = (int(ob.pt[0]), int(ob.pt[1]))
    if pt not in left_matches:
        left_count[pt[0]//100][pt[1]//100] += 1
    elif pt in left_matches and dist(pt, kp2[left_matches[pt]].pt):
        left_count[pt[0]//100][pt[1]//100] += 1

for ob in kp2:
    pt = (int(ob.pt[0]), int(ob.pt[1]))
    if pt not in right_matches:
        right_count[(pt[0])//100][(pt[1])//100] += 1
    elif pt in right_matches and dist(pt, kp1[right_matches[pt]].pt):
        right_count[(pt[0])//100][(pt[1])//100] += 1



def rcolor():
    return (np.random.randint(0, 256),np.random.randint(0, 256),np.random.randint(0, 256))


for r in range(len(left_count)):
    for c in range(len(left_count[r])):
        if (left_count[r][c] > COUNT_THRESHOLD):
            if clr == "rnd":
                color = rcolor()
                cv2.circle(img3, (r*100+50, c*100+50), left_count[r][c]*w//RADIUS_DIVISOR, color, (left_count[r][c]+1)*w//STROKE_DIVISOR) #only adding 50 means at BOTTOM RIGHT corner the +50 pushes out of screen if last box is 20x20 say for 1020x1020 e.g..
                cv2.circle(img3, (r*100+50+w, c*100+50), left_count[r][c]*w//RADIUS_DIVISOR, color, (left_count[r][c]+1)*w//STROKE_DIVISOR) #TODO GOTTA INCORPORATE #s of COUNT INTO CALC AS WELL
            elif clr == "rgb":
                cv2.circle(img3, (r*100+50, c*100+50), left_count[r][c]*w//RADIUS_DIVISOR, (240, 140, 10), (left_count[r][c]+1)*w//STROKE_DIVISOR) #only adding 50 means at BOTTOM RIGHT corner the +50 pushes out of screen if last box is 20x20 say for 1020x1020 e.g..
                cv2.circle(img3, (r*100+50+w, c*100+50), left_count[r][c]*w//RADIUS_DIVISOR, (240, 10, 10), (left_count[r][c]+1)*w//STROKE_DIVISOR) #TODO GOTTA INCORPORATE #s of COUNT INTO CALC AS WELL

for r in range(len(right_count)):
    for c in range(len(right_count[r])):
        if (right_count[r][c] > COUNT_THRESHOLD):
            if clr == "rnd":
                color = rcolor()
                cv2.circle(img3, (r*100+50, c*100+50), right_count[r][c]*w//RADIUS_DIVISOR, color, (right_count[r][c]+1)*w//STROKE_DIVISOR) #only adding 50 means at BOTTOM RIGHT corner the +50 pushes out of screen if last box is 20x20 say for 1020x1020 e.g..
                cv2.circle(img3, (r*100+50+w, c*100+50), right_count[r][c]*w//RADIUS_DIVISOR, color, (right_count[r][c]+1)*w//STROKE_DIVISOR)
            elif clr == "rgb":
                cv2.circle(img3, (r*100+50, c*100+50), right_count[r][c]*w//RADIUS_DIVISOR, (10, 240, 140), (right_count[r][c]+1)*w//STROKE_DIVISOR) #only adding 50 means at BOTTOM RIGHT corner the +50 pushes out of screen if last box is 20x20 say for 1020x1020 e.g..
                cv2.circle(img3, (r*100+50+w, c*100+50), right_count[r][c]*w//RADIUS_DIVISOR, (10, 240, 10), (right_count[r][c]+1)*w//STROKE_DIVISOR)

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
