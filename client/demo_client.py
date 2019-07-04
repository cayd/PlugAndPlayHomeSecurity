from socketIO_client import SocketIO, LoggingNamespace
#from camera import VideoCamera
import cv2
import numpy as np

#def grab_frame(camera):
#    frame = camera.get_frame()
#    return (b'--frame\r\n'
#            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n').encode('base64')

#def video_feed():
#    return grab_frame(VideoCamera())

def on_frame_response(args):
    print('frame response:', args['data'])


socketIO = SocketIO('localhost', 8000, LoggingNamespace)
socketIO.on('frame_ack', on_frame_response)

video = cv2.VideoCapture(0)
while True:
    success, image = video.read()
    ret, jpeg = cv2.imencode('.jpg', image)

    nparr = np.fromstring(jpeg, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    

    args = { 'frame' : jpeg.tobytes().encode('base64') }
    print("emission")

    socketIO.emit('frame', args)
    socketIO.wait(seconds=1)
