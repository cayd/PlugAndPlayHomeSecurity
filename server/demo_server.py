from flask import Flask, render_template, Response, send_from_directory, url_for, request
from flask_socketio import SocketIO, emit
from camera import VideoCamera
import numpy as np
import cv2, os, datetime

app = Flask(__name__)
socketio = SocketIO(app)


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
        file = cv2.imread('static/' + stream_id + '_frame.jpg',0)
        ret, jpeg = cv2.imencode('.jpg', file)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        

# stream_id should match with a client name. if that is not the case, then we default to 
# the server feed
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


@socketio.on('frame')
def handle_frame(args):
    client_frame=args['frame'].decode('base64')
    client_name=args['sender'] 
    print("got frame from " + client_name)

    # image conversion from bytes
    nparr = np.fromstring(client_frame, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imwrite('static/' + client_name  + '_frame.jpg',img) 

    emit("frame_ack", { 'data' : 'Thank You!'} ) #can get rid of this once done debugging

    # logging
    global logs_table, last_log
    if (client_name in logs_table):
        logs_table[client_name].write(img)
    else:
        height , width , layers =  img.shape
        logs_table[client_name] = cv2.VideoWriter('logs/' + client_name + '.avi',-1,1,(width,height))
        logs_table[client_name].write(img)
        #cv2.destroyAllWindows()
        #video.release()

    # if more than a minute has passed since the last logging, dump the log
    #if datetime.datetime.now() > last_log + timedelta(minutes=1):
        
    
        
if __name__ == '__main__':
    
    #set up data structures for logging 
    global logs_table, last_log 
    logs_table = {  }
    last_log = datetime.datetime.now()

    #run the server
    socketio.run(app, host='0.0.0.0', debug=True, port=int("8000"))

