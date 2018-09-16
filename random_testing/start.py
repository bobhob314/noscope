from bottle import route, run, template, post, request

@route('/hello')
def hello():
    return "Hello World!"

@route('/')
@route('/hello/<name>')
def greet(name='Stranger'):
    return template('Hello {{name}}, how are you?', name=name)


@post('/login') # or @route('/login', method='POST')
def do_login():
    name = "asDASDAs"
    print ("username is")
    username = request.forms.get('username')
    password = request.forms.get('password')
    return template('username: {{username}}, password: {{password}}', username = username, password=password )


run(host='localhost', port=3000, debug=True)
