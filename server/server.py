from cam_socket import run_cam_socket
from web_server import run_web_server

from threading import Thread


def main():
    Thread(target=run_cam_socket, kwargs=dict(p=8001)).start() 
    Thread(target=run_web_server).start()


if __name__ == '__main__':
    main()
