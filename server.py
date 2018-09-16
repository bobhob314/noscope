from bottle import Bottle, route, run, error
from bottle import template, request, get, post, static_file
import bottle

bottle.debug(True)


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static/')

@route('/')
def index():
    return template('index')

@route('/welcome.php')
def welcome():
    return template('welcome.php')

@route('/hello/<name>')
def greet(name='Stranger'):
    return template('Hello {{name}}, how are you?', name=name)
@route('/hello')
def hello():
    return "Hello World!"

@get('/login') # or @route('/login')
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

@post('/login')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        return "<p>Your login information was correct.</p>"
    else:
        return "<p>Login failed.</p>"

@route('/test')
def test():
    return static_file('index.html', './website')

run(host='localhost', port=8080, debug=True, reloaded=True)
