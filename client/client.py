from socketIO_client import SocketIO, LoggingNamespace
import cv2, time
import numpy as np


def on_frame_response(args):
    print('frame response:', args['data'])


def main():
    # generate the client name. If none can be produced from the client's file, then
    # use a timestamp 
    client_name = ""
    try:
        with open("client_file.txt", 'r') as f:
            list = f.readlines()
            client_name = list[0]
    except:
        client_name = str(time.time())
        with open("client_file.txt", 'w') as f:
            f.write(client_name)

    print("Booting Client " + client_name)
    

    # main event loop sends packets until connection is lost
    # at which point it blocks polling for the socket
    #while True:
    #try: 
    socketIO = SocketIO('localhost', 8001, LoggingNamespace)
    socketIO.on('frame_ack', on_frame_response)
    #except:
    #    continue

    video = cv2.VideoCapture(0)
    while True:
        success, image = video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        
        args = { 'frame' : jpeg.tobytes().encode('base64'), 'sender' : client_name } #.encode
        print("emission")
            
        #try:
        socketIO.emit('frame', args)
        socketIO.wait(seconds=.02)
        #except:
        #    break


if __name__ == '__main__':
    main()
