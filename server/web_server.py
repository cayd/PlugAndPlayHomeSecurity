from flask import Flask, render_template, Response, send_from_directory, url_for, request
from camera import VideoCamera
import numpy as np
import cv2, os, datetime
import settings

app = Flask(__name__)

@app.route("/")
def login_page():
    return "Please Authenticate"

@app.route("/logged_in")
def stream_selector():
    return "View your streams or register a new device"

@app.route("/register_device")
def register():
    return "A download will start on your computer. Just run the executable once completed"

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/server_feed')
def server_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def gen_client(stream_id):
    while True:
        settings.img_lock.acquire()
        file = cv2.imread('static/' + stream_id + '_frame.jpg',0)
        settings.img_lock.release()
        ret, jpeg = cv2.imencode('.jpg', file)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        

# stream_id should match with a client name. if that is not the case, then we default to 
# the server feed 
#TODO: default should be changed to all streams chosen for the dashboard by the authenticated user
@app.route('/client_feed')
def client_feed():
    try:
        stream_id=request.args['stream_id']
        if not os.path.isfile('static/' + stream_id + '_frame.jpg'):
            raise Exception("not a valid stream_id. default to server feed")
        return Response(gen_client(stream_id),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    except: 
        return server_feed()


def run_web_server():    
    #run the server
    app.run(host='0.0.0.0', debug=False, port=8000)

