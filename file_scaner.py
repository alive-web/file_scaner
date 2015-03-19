import argparse
import asyncore
import pyinotify
from db import DataBase

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path',  type=str, required=True, help='path to scan directory')
args = parser.parse_args()
watched_dir = args.path
wm = pyinotify.WatchManager()
database = DataBase()
mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_ATTRIB | pyinotify.IN_CLOSE_WRITE


class EventHandler(pyinotify.ProcessEvent):
    def __init__(self, db, **kwargs):
        super(EventHandler, self).__init__(**kwargs)
        self.db = db

    def process_default(self, event):
        self.db.write_log(event)

pyinotify.AsyncNotifier(wm, EventHandler(database))
wm.add_watch(watched_dir, mask, rec=True)

asyncore.loop()