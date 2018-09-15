from bottle import Bottle, route, run
from bottle import template, request, get, post, static_file

@route('/')
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

@post('/login')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        return "<p>Your login information was correct.</p>"
    else:
        return "<p>Login failed.</p>"

run(host='localhost', port=8080, debug=True)
