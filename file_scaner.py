import argparse
import asyncore
import pyinotify
from datetime import datetime
from pymongo import MongoClient


parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path',  type=str, required=True, help='path to scan directory')
args = parser.parse_args()
watched_dir = args.path

client = MongoClient('localhost', 27017)
db = client.file_scaner
events = db.events
wm = pyinotify.WatchManager()

def write_log_in_db(event):
    # This function will accept one argument "event" and will record in db
    action = {
        'edited': datetime.now(),
        'event': event.maskname,
        'file': event.pathname
    }
    events.insert(action)


def create_copy():
    # This function will accept one argument "path to file" and will record reserve copy file in db
    pass

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        write_log_in_db(event)
        if event.dir:
            # restart loop
            pass

    def process_IN_DELETE(self, event):
        write_log_in_db(event)

    def process_IN_CLOSE_WRITE(self, event):
        write_log_in_db(event)

    def process_IN_ATTRIB(self, event):
        write_log_in_db(event)

notifier = pyinotify.AsyncNotifier(wm, EventHandler())
wdd = wm.add_watch(watched_dir, pyinotify.ALL_EVENTS, rec=True)

asyncore.loop()