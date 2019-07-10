from flask import Flask, render_template, Response, send_from_directory, url_for, request
from flask_socketio import SocketIO, emit
from camera import VideoCamera
import numpy as np
import cv2, os, datetime
from threading import Thread, Lock

import settings.settings as settings

app = Flask(__name__)
socketio = SocketIO(app, async_handlers=True)

# args: name of the intended log feed, 
#       img0 first image of the feed. used for sizing
# returns: a log feed
def make_log_feed(name, img0):
    codec = cv2.VideoWriter_fourcc('D','I','V','X')
    print(codec)
    
    #size = (int(img0.get(cv2.CAP_PROP_FRAME_WIDTH)),
    #        int(img0.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    h, w, _ = img0.shape
    print(w, h)
    videoFile = cv2.VideoWriter();
    videoFile.open(name, codec, 25, (w,h), 1)
    return videoFile

@socketio.on('frame')
def handle_frame(args):
    client_frame=args['frame'].decode('base64')

    client_name=args['sender']
    print("got frame from " + client_name)

    # image conversion from bytes
    nparr = np.fromstring(client_frame, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    try:
        settings.locks_map[client_name].acquire()
    except:
        settings.locks_map[client_name] = Lock()
        settings.locks_map[client_name].acquire()

    cv2.imwrite('static/' + client_name  + '_frame.jpg',img)
    settings.locks_map[client_name].release()

    emit("frame_ack", { 'data' : 'Thank You!'} ) #can get rid of this once done debugging

    # logging
    if (client_name in settings.logs_map):
        print("writing img")
        settings.logs_map[client_name].write(img)
    else:
        settings.logs_map[client_name] = make_log_feed('logs/'+client_name+'_'+ str(datetime.datetime.now().isoformat())+'.avi', img) 
        settings.logs_map[client_name].write(img)


    # if more than a minute has passed since the last logging, write out the log
    if datetime.datetime.now() > settings.last_log + datetime.timedelta(minutes=1):
        print("dumping logs out now")
        print(settings.logs_map)
        for name, log in settings.logs_map.items():
            cv2.destroyAllWindows()
            log.release()
            settings.last_log = datetime.datetime.now()
            settings.logs_map[client_name] = make_log_feed('logs/'+client_name+'_'+ str(datetime.datetime.now().isoformat())+'.avi', img)
            settings.logs_map[client_name].write(img)

#p is a port number. it is typically passed in from the command line
def run_cam_socket(p=8002):
    #run the server
    socketio.run(app, host='0.0.0.0', debug=False, port=p)
