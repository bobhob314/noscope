from bottle import route , run

@route('/hello')
def hello():
    return "Hello World"

run(host='localhost', port=3000, debug=True)
