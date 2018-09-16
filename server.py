import json

from bottle import static_file, redirect, run, Bottle, request, response, BaseRequest, template, route, get, post
from gridfs import GridFS
from pymongo import MongoClient

# TODO currently they have to be the same size lmao

BaseRequest.MEMFILE_MAX = 1024 * 1024 * 1024
FILE_API = Bottle()
MONGO_CLIENT = MongoClient('mongodb://localhost:27017/')
DB = MONGO_CLIENT['noscope']
GRID_FS = GridFS(DB)

file1 = ""
file2 = ""

@FILE_API.get('/')
def index():
    return template('index')

@FILE_API.get('/static/<filepath:path>')
def static_server(filepath):
    return static_file(filepath, root='./static/')

@FILE_API.get('/views/<filepath:path>')
def static_server(filepath):
    return static_file(filepath, root='./views/')

@FILE_API.get('/welcome.php')
def welcome():
    print("FOR FUCCCCKSS")
    return template('welcome')
    # return template('welcome.php')

@FILE_API.post('/welcome.php')
def do_welcome():
    print("OH FOR FUCKS SAKE")
    #return "<p>"+request.forms.get('fileupload1')+"</p>"
    file1 = request.forms.get('fileupload1')
    file2 = request.forms.get('fileupload2')
    clr = request.forms.get('color')
    griddify = request.forms.get('griddify')
    print(file1, file2)
    if (not griddify): griddify = "-"
    return redirect('/compare/'+file1+'/'+file2+'/'+clr+'/'+griddify)
    # return template('welcome.php')

#########################33

@FILE_API.get('/compare/<file1>/<file2>/<clr>/<griddify>')
def compare(file1, file2, clr, griddify):

    import cv2
    import numpy as np
    from matplotlib import pyplot as plt
    import os, sys

    '''
    fn1 = sys.argv[1]
    fn2 = sys.argv[2]
    clr = sys.argv[3]
    print(str(fn1), str(fn2))
    '''

    #TODO what if no arguments given or not proper ones

    # TODO AUTOMATE THRESHOLDS!!!! AND MULTIPLICATIVE FACTORS!!
    sift = cv2.xfeatures2d.SIFT_create()

    #img1
    img1 = cv2.imread(file1)
    gray1= cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    kp1, des1 = sift.detectAndCompute(gray1,None)
    #img1=cv2.drawKeypoints(gray1,kp1,img1)
    #cv2.imwrite('1sift_keypoints.jpg',img1)
    #img1=cv2.drawKeypoints(gray1,kp1,img1,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    #cv2.imwrite('1sift_keypoints2.jpg',img1)

    #img2
    img2 = cv2.imread(file2)
    gray2= cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    kp2, des2 = sift.detectAndCompute(gray2,None)
    #img2=cv2.drawKeypoints(gray2,kp2,img2)
    #cv2.imwrite('2sift_keypoints.jpg',img2)
    #img2=cv2.drawKeypoints(gray2,kp2,img2,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    #cv2.imwrite('2sift_keypoints2.jpg',img2) # kinda repeated. here and above.

    h, w = (int(img1.shape[0]), int(img1.shape[1]))

    SIZE_BOUND = 50 - 50  # TODO!!!! IF I CHANGE THIS SIZE MAYBE THERE WILL BE CORRESPONDING TINGS
    print(len(kp1), len(kp2))
    cnt1 = 0
    cnt2 = 0

    for ob in kp1:
        if ob.size >= SIZE_BOUND:
            cnt1 += 1
    for ob in kp2:
        if ob.size >= SIZE_BOUND:
            cnt2 += 1
    print(cnt1, cnt2)
    average_features = (cnt1+cnt2)//2
    if (griddify == "-"):
        COUNT_THRESHOLD = average_features//300 # pretty sure should be exponential but hey
        RADIUS_DIVISOR = average_features//2
        STROKE_DIVISOR = average_features*8
    else:
        COUNT_THRESHOLD = average_features*3000//w//300 # pretty sure should be exponential but hey
        RADIUS_DIVISOR = average_features*15000//w//2
        STROKE_DIVISOR = average_features*9000//w//8


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

    left_count = [[0 for i in range(h//100+1)] for j in range(w//100+1)] # +1 bc why not
    right_count = [[0 for i in range(h//100+1)] for j in range(w//100+1)]

    DELTA_THRESHOLD = 80 # only show matches if above delta (movement) THRESHOLDS
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



    def rcolor():
        return (np.random.randint(0, 256),np.random.randint(0, 256),np.random.randint(0, 256))

    print("matches", len(matches))
    print("left matches", len(left_matches))

    print("kp1 len", len(kp1))
    for ob in kp1:
        pt = ob.pt
        intpt = tuple(map(int, pt))
        if pt not in left_matches:
            #continue # DELETE!!!
            left_count[intpt[0]//100][intpt[1]//100] += 1
        elif pt in left_matches and dist(pt, kp2[left_matches[pt].trainIdx].pt) > DELTA_THRESHOLD: # queryidx trainidx switches?
            #cv2.circle(img3, tuple(map(int, ob.pt)), 20, rcolor(), 15)
            left_count[intpt[0]//100][intpt[1]//100] += 1

    for ob in kp2:
        #cv2.circle(img3, tuple(map(int, (ob.pt[0]+w, ob.pt[1]))), 20, rcolor(), 15)
        pt = ob.pt
        intpt = tuple(map(int, pt))
        if pt not in right_matches:
            #continue # DELETE!!!
            right_count[(intpt[0])//100][(intpt[1])//100] += 1
        elif pt in right_matches and dist(pt, kp1[right_matches[pt].queryIdx].pt) > DELTA_THRESHOLD:
            right_count[(intpt[0])//100][(intpt[1])//100] += 1



    for r in range(len(left_count)):
        for c in range(len(left_count[r])):
            if (left_count[r][c] > COUNT_THRESHOLD):
                if clr == "rnd":
                    color = rcolor()
                    cv2.circle(img3, (r*100+50, c*100+50), left_count[r][c]*w//RADIUS_DIVISOR, color, (left_count[r][c]+1)*w//STROKE_DIVISOR) #only adding 50 means at BOTTOM RIGHT corner the +50 pushes out of screen if last box is 20x20 say for 1020x1020 e.g..
                    cv2.circle(img3, (r*100+50+w, c*100+50), left_count[r][c]*w//RADIUS_DIVISOR, color, (left_count[r][c]+1)*w//STROKE_DIVISOR) #TODO GOTTA INCORPORATE #s of COUNT INTO CALC AS WELL
                elif clr == "rgb":
                    cv2.circle(img3, (r*100+50, c*100+50), left_count[r][c]*w//RADIUS_DIVISOR, (50, 140, 240), (left_count[r][c]+1)*w//STROKE_DIVISOR) #only adding 50 means at BOTTOM RIGHT corner the +50 pushes out of screen if last box is 20x20 say for 1020x1020 e.g..
                    cv2.circle(img3, (r*100+50+w, c*100+50), left_count[r][c]*w//RADIUS_DIVISOR, (10, 10, 240), (left_count[r][c]+1)*w//STROKE_DIVISOR) #TODO GOTTA INCORPORATE #s of COUNT INTO CALC AS WELL
                    # the order of RGB in local is BGR in htmll.... dafaq #1: ? #2: browser righ red
    for r in range(len(right_count)):
        for c in range(len(right_count[r])):
            if (right_count[r][c] > COUNT_THRESHOLD):
                if clr == "rnd":
                    color = rcolor()
                    cv2.circle(img3, (r*100+50, c*100+50), right_count[r][c]*w//RADIUS_DIVISOR, color, (right_count[r][c]+1)*w//STROKE_DIVISOR) #only adding 50 means at BOTTOM RIGHT corner the +50 pushes out of screen if last box is 20x20 say for 1020x1020 e.g..
                    cv2.circle(img3, (r*100+50+w, c*100+50), right_count[r][c]*w//RADIUS_DIVISOR, color, (right_count[r][c]+1)*w//STROKE_DIVISOR)
                elif clr == "rgb":
                    cv2.circle(img3, (r*100+50, c*100+50), right_count[r][c]*w//RADIUS_DIVISOR, (140, 240, 10), (right_count[r][c]+1)*w//STROKE_DIVISOR) #only adding 50 means at BOTTOM RIGHT corner the +50 pushes out of screen if last box is 20x20 say for 1020x1020 e.g..
                    cv2.circle(img3, (r*100+50+w, c*100+50), right_count[r][c]*w//RADIUS_DIVISOR, (10, 130, 10), (right_count[r][c]+1)*w//STROKE_DIVISOR)
                    # #1: green left. 2: green right. DAFAQ.
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

    #plt.imshow(img3), plt.show()
    cv2.imwrite('static/output.jpg', img3)


    return template('comparetemplate', file1=file1, file2=file2) # , filename='output.jpg' RN hardcoded ot be output.jpg
    return "<p>Now done comparing images "+file1+" and "+file2+"</p>"

################################3

@FILE_API.route('/hello/<name>')
def greet(name='Stranger'):
    return template('Hello {{name}}, how are you?', name=name)

@FILE_API.route('/hello')
def hello():
    return "Hello World!"

@FILE_API.get('/login') # or @route('/login')
def login():
    return static_file('login.html', '.')

def check_login(username, password):
    return True

# @route('/<filename:path>')
# def server_static(filename):
#     return static_file(filename, root='./website')

# @route('/<page>')
# def server_static(filename):
#     print('{{page}}')
#     return static_file(filename, root='./website/{{page}}')

@FILE_API.post('/login')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        return "<p>Your login information was correct.</p>"
    else:
        return "<p>Login failed.</p>"


@FILE_API.post('/upload')
def upload():
    category = request.forms.get('category')
    upload = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.png', '.jpg', '.jpeg'):
        return "File extension not allowed."

    save_path = "/tmp/{category}".format(category=category)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
    upload.save(file_path)
    return "File successfully saved to '{0}'.".format(save_path)


    '''
    image = request.files.get('image')
    file_id = GRID_FS.put(image.file, file_name="testimage")
    # If the file is found in the database then the save
    # was successful else an error occurred while saving.
    if GRID_FS.find_one(file_id) is not None:
        return json.dumps({'status': 'File saved successfully'})
    else:
        response.status = 500
        return json.dumps({'status': 'Error occurred while saving file.'})
    '''

@FILE_API.post('/user')
def upload():
    username = request.forms.get('username')
    password = request.forms.get('password')
    file_id = GRID_FS.put(image.file, file_name="testimage")
    # If the file is found in the database then the save
    # was successful else an error occurred while saving.
    if GRID_FS.find_one(file_id) is not None:
        return json.dumps({'status': 'File saved successfully'})
    else:
        response.status = 500
        return json.dumps({'status': 'Error occurred while saving file.'})



run(app=FILE_API, host='localhost', port=3000, reloader=True)
