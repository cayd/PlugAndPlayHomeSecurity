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

    global users_map
    users_map = { }
    #print("hi")
    with open('settings/user_list.txt', 'r') as f:
        lines=f.readlines()
        #print('lines', lines)
        for i in lines:
            line=i.split(',')
            users_map[line[0].strip()] = line[1].strip()

    global feeds
    feeds=[]

def next_available_port():
    global ports_map
    
    largest_port = -1
    for name, port in ports_map.items():
        if port > largest_port:
            largest_port = port

    return largest_port
    
