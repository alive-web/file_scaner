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


class EventHandler(pyinotify.ProcessEvent):
    def __init__(self, db, **kwargs):
        super(EventHandler, self).__init__(**kwargs)
        self.db = db

    def process_IN_ALL_EVENTS(self, event):
        self.db.write_log(event)

pyinotify.AsyncNotifier(wm, EventHandler(database))
wm.add_watch(watched_dir, pyinotify.ALL_EVENTS, rec=True)

asyncore.loop()