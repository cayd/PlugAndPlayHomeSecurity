from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
from camera import VideoCamera
import numpy as np
import cv2

app = Flask(__name__)
socketio = SocketIO(app)

global client_frame
client_frame=None

@app.route("/")
def login_page():
    return "Please Authenticate"

@app.route("/logged_in")
def stream_selector():
    return "Choose a stream to view"

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/server_feed')
def server_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def gen_client(frame):
    return frame

@app.route('/client_feed')
def client_feed():
    print("viewing client feed")
    global client_frame

    nparr = np.fromstring(client_frame, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    cv2.imshow('image', img)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()

    return Response(client_frame, mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('frame')
def handle_frame(args):
    print("got frame", args)
    global client_frame
    client_frame=args['frame'].decode('base64')
    # try to show image here 
    emit("frame_ack", { 'data' : 'Thank You!'} )

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True, port=int("8000"))
    #app.run(host='0.0.0.0', debug=True, port="33")
