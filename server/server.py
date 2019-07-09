from cam_socket import run_cam_socket
from web_server import run_web_server
import settings.settings as settings

from threading import Thread, Lock


def main():
    settings.init()
    Thread(target=run_web_server).start()
    Thread(target=run_cam_socket, kwargs=dict(p=8001)).start() 

if __name__ == '__main__':
    main()
