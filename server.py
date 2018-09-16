import json

from bottle import static_file, run, Bottle, request, response, BaseRequest, template, route, get, post
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

@FILE_API.get('/static/<filepath:path>')
def static_server(filepath):
    return static_file(filepath, root='./static/')

@FILE_API.get('/welcome')
def welcome():
    return template('welcome.php')
    # return template('welcome.php')

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



run(app=FILE_API, host='localhost', port=3000, reloader=True)
