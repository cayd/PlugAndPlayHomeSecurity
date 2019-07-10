from threading import Lock
import datetime

def init():
    global locks_map, logs_map
    locks_map, logs_map = { }, { }
    with open('settings/client_list.txt', 'r') as f:
        lines = f.readlines()
        for i in lines:
            line = i.split(',')
            locks_map[line[0].strip()]=Lock()

    global last_log
    last_log = datetime.datetime.now()

    global authenticated_users_list
    authenticated_users_list = []


#def next_available_port():
#    global ports_map
#    
#    largest_port = -1
#    for name, port in ports_map.items():
#        if port > largest_port:
#            largest_port = port
#
#    return largest_port
    
