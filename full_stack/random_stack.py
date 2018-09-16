import json

from bottle import run, Bottle, request, response, BaseRequest, template
from gridfs import GridFS
from pymongo import MongoClient

BaseRequest.MEMFILE_MAX = 1024 * 1024 * 1024
FILE_API = Bottle()
MONGO_CLIENT = MongoClient('mongodb://localhost:27017/')
DB = MONGO_CLIENT['noscope']
GRID_FS = GridFS(DB)

@FILE_API.get('/')
def index():
    return template('index')



run(app=FILE_API, host='localhost', port=3000)
