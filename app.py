from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('aaa')
def test_connect():
    print("Welcome, aaa received")
    emit('aaa_response', {'data': 'Server'})

if __name__ == '__main__':
    socketio.run(app, port=8000)
