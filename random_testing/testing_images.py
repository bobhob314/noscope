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
    image = request.files.get('image')
    file_id = GRID_FS.put(image.file, file_name="testimage")
    # If the file is found in the database then the save
    # was successful else an error occurred while saving.
    if GRID_FS.find_one(file_id) is not None:
        return json.dumps({'status': 'File saved successfully'})
    else:
        response.status = 500
        return json.dumps({'status': 'Error occurred while saving file.'})

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

run(app=FILE_API, host='localhost', port=3000)
