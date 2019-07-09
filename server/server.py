from cam_socket import run_cam_socket
from web_server import run_web_server
from registration_server import run_registration_server
import settings.settings as settings

from threading import Thread, Lock


def main():
    settings.init()
    Thread(target=run_web_server).start()
    Thread(target=run_registration_server).start()

    #start threads for each of the clients that are in the settings file
    for id, port in settings.ports_map.items():
        print(id, port)
        Thread(target=run_cam_socket, kwargs=dict(p=port)).start()
        

if __name__ == '__main__':
    main()
