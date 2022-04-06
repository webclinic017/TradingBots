import os
import pprint
import json as _json
import time
from datetime import datetime

def get_datetime():
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

start_st = get_datetime()
logFile = None

def init(logFileName):
    global logFile
    path = os.path.dirname(os.path.realpath(__file__))
    logFile = open('{}/logs/{}-{}.log'.format(path, logFileName, start_st), 'a')
    print(f'log file {logFile}')

def formatMsg(msg, df=False, json=False):
    st = get_datetime()
    if not df and not json:
        entry = f'{st}: {msg}\n'
    elif df:
        entry = f'{st}\n{msg}\n'
    elif json:
        json_msg = _json.dumps(msg)
        entry =  f'{{"datetime": "{st}", "portfolio": {json_msg}}}\n' 
    return entry

def write(msg, df=False, json=True, print_it=True):
    global logFile
    entry = formatMsg(msg, df, json)
    logFile.write(entry)
    logFile.flush()

    if print_it:
    	print(entry.strip())

def appendTo(logFileName, msg):
    path = os.path.dirname(os.path.realpath(__file__))
    logFile = open('{}/logs/{}.log'.format(path, logFileName), 'a')
    entry = formatMsg(msg, json=True)
    logFile.write(entry)
    logFile.flush()
    logFile.close()


