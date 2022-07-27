from flask import Flask, jsonify, request
from gevent import pywsgi
app = Flask(__name__)

@app.route('/register', methods = ['POST'])
def register():
    print(request)
    print(request.environ)
    print(request.data)
    response = jsonify({'Hello': 'world!'})
    print(response)
    print(response.data)
    return response

if __name__ == '__main__':
    server = pywsgi.WSGIServer(('127.0.0.1',5000),app)
    server.serve_forever()