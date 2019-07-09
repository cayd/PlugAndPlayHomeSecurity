from threading import Lock
import datetime

def init():
    global ports_map, locks_map
    ports_map, locks_map = { }, { }
    with open('settings/client_list.txt', 'r') as f:
        lines = f.readlines()
        for i in lines:
            line = i.split(',')
            ports_map[line[0].strip()]=int(line[1].strip())
            locks_map[line[0].strip()]=Lock()
    print(ports_map)


    global img_lock
    img_lock = Lock()

    global logs_map, last_log
    logs_map = { }
    last_log = datetime.datetime.now()
