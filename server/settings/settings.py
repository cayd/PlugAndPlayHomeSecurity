from threading import Lock
import datetime

def init():
    #todo convert lock to a dictionary of locks. More scalable
    global img_lock
    img_lock = Lock()

    global logs_table, last_log
    logs_table = { }
    last_log = datetime.datetime.now()
