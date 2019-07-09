from flask import Flask, render_template, Response, send_from_directory, url_for, request
from flask_socketio import SocketIO, emit
from camera import VideoCamera
import numpy as np
import cv2, os, datetime
from threading import Thread

import settings.settings as settings

app = Flask(__name__)
socketio = SocketIO(app, async_handlers=True)

@socketio.on('frame')
def handle_frame(args):
    client_frame=args['frame'].decode('base64')

    client_name=args['sender']
    print("got frame from " + client_name)

    # image conversion from bytes
    nparr = np.fromstring(client_frame, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    settings.img_lock.acquire()
    cv2.imwrite('static/' + client_name  + '_frame.jpg',img)
    settings.img_lock.release()

    emit("frame_ack", { 'data' : 'Thank You!'} ) #can get rid of this once done debugging

    # logging
    if (client_name in settings.logs_table):
        settings.logs_table[client_name].write(img)
    else:
        height , width , layers =  img.shape
        settings.logs_table[client_name] = cv2.VideoWriter('logs/' + client_name + '.avi',-1,1,(width,height))
        settings.logs_table[client_name].write(img)
        #cv2.destroyAllWindows()
        #video.release()

    # if more than a minute has passed since the last logging, dump the log
    #if datetime.datetime.now() > last_log + timedelta(minutes=1):


#p is a port number. it is typically passed in from the command line
def run_cam_socket(p=8001):
    #run the server
    socketio.run(app, host='0.0.0.0', debug=False, port=p)
