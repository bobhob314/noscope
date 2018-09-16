import json

from bottle import run, Bottle, request, response, BaseRequest
from gridfs import GridFS
from pymongo import MongoClient

BaseRequest.MEMFILE_MAX = 1024 * 1024 * 1024
FILE_API = Bottle()
MONGO_CLIENT = MongoClient('mongodb://localhost:27017/')
DB = MONGO_CLIENT['noscope']
GRID_FS = GridFS(DB)

@FILE_API.post('/upload')
def upload():
    print(type(request.files.get('image')))
    image = request.files.get('image')
    filename = image.filename
    file_id = GRID_FS.put(image.file, file_name=file_name)
    # If the file is found in the database then the save
    # was successful else an error occurred while saving.
    if GRID_FS.find_one(file_id) is not None:
        return json.dumps({'status': 'File saved successfully'})
    else:
        response.status = 500
        return json.dumps({'status': 'Error occurred while saving file.'})

@FILE_API.get('/download/<filename>')
def download(filename):
    print (filename)
    grid_fs_file = GRID_FS.find_one({'file_name': filename})
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename)
    print(type(grid_fs_file))
    if grid_fs_file:
        print ("Found the file !!!")
    else:
        print ("Sadlife")
    return grid_fs_file


<<<<<<< HEAD
run(app=FILE_API, host='localhost', port=3000, reloader = True)
=======
@FILE_API.get('/')
def index():
    return template('index')

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='/views')


run(app=FILE_API, host='localhost', port=3000)
>>>>>>> origin/CSS_Move
