from socketIO_client import SocketIO, LoggingNamespace
import cv2, time
import numpy as np
from threading import Lock

def on_frame_response(args):
    print('frame response:', args['data'])

def on_registration_response(args):
    print('registration response:', args)


def main():
    # generate the client name. If none can be produced from the client's file, then
    # use a timestamp 
    client_name = ""
    try:
        with open("client_file.txt", 'r') as f:
            list = f.readlines()
            client_name = list[0].strip()
    except:
        #register a new client
        print("registering as a new client")
        client_name = str(time.time())        
        args = { 'sender' : client_name }

        socketIO = SocketIO('http://boingoreg.ngrok.io')
        socketIO.on('registration_ack', on_frame_response)
        socketIO.emit('registration_request', args)

        with open("client_file.txt", 'w') as f:
            f.write(client_name)

    print("Booting Client " + client_name)
    

    # main event loop sends packets until connection is lost
    # at which point it blocks polling for the socket
    #while True:
    #try: 
    socketIO = SocketIO('http://boingocam.ngrok.io')#'http://boingocam.ngrok.io'
    socketIO.on('frame_ack', on_frame_response)
    #except:
    #    continue

    video = cv2.VideoCapture(0)
    while True:
        success, image = video.read()
        if not success:
            continue

        ret, jpeg = cv2.imencode('.jpg', image)
        
        args = { 'frame' : jpeg.tobytes().encode('base64'), 'sender' : client_name } 
        print("emission")
            
        #try:
        socketIO.emit('frame', args)
        socketIO.wait(seconds=.5)
        #except:
        #    break


if __name__ == '__main__':
    main()
