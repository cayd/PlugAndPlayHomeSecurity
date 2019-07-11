from flask import Flask, render_template, Response, send_from_directory, url_for, request
from camera import VideoCamera
import numpy as np
import cv2, os, datetime
import settings.settings as settings

app = Flask(__name__)

@app.route("/")
def login_page():
    return render_template("login.html")
    #return "Please Authenticate"

@app.route("/logged_in")
def stream_selector():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Go to Streams':
            return "opt1"
            return redirect(url_for('client_feed'))
        elif request.form['submit_button'] == 'Register a New Device':
            return "opt2"
            return redirect(url_for('register'))
        else: 
            return "failed"
    elif request.method == 'GET':
        return render_template("logged_in.html")

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
        settings.locks_map[stream_id].acquire()
        file = cv2.imread('static/' + stream_id + '_frame.jpg',0)
        settings.locks_map[stream_id].release()
        ret, jpeg = cv2.imencode('.jpg', file)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        

# stream_id should match with a client name. if that is not the case, then we default to 
# the server feed 
#TODO: default should be changed to all streams chosen for the dashboard by the authenticated user
@app.route('/show_clients')
def show_clients(stream_id=None):
    #if user not in settings.authenticated_user_list:
    #    return "can't view, log in first"
    print("s_id", stream_id)
    try:
        #stream_id=request.args['stream_id']
        if not (os.path.isfile('static/' + stream_id + '_frame.jpg') and 
                stream_id in settings.locks_map):
            raise Exception("not a valid stream_id. default to server feed")
        return Response(gen_client(stream_id),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    except: 
        return server_feed()
        
def find_all_feeds():
    feeds = []
    for i in settings.locks_map:
        feeds.append(i)
    print("feeds", feeds)
    return feeds

@app.route('/client_feed')
def client_feed():
    try:
        f = [ request.args['stream_id'] ]
    except:
        f = find_all_feeds()
        print("finding all feeds")
    print(f)
    return render_template('video_feeds.html', feeds=f)


def run_web_server():    
    #run the server
    app.run(host='0.0.0.0', debug=False, port=8000)
