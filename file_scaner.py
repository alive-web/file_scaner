import argparse
import asyncore
import pyinotify
from tree import build_tree
from db import DataBase


parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path',  type=str, required=True, help='path to scan directory')
args = parser.parse_args()
watched_dir = args.path
wm = pyinotify.WatchManager()
database = DataBase()
tree = build_tree(watched_dir)
if tree:
    for document in tree:
        database.create_new(document["pathname"], document["is_dir"], watched_dir)
mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_ATTRIB \
       | pyinotify.IN_CLOSE_WRITE | pyinotify.IN_MOVED_TO | pyinotify.IN_MOVED_FROM


class EventHandler(pyinotify.ProcessEvent):
    def __init__(self, db, **kwargs):
        super(EventHandler, self).__init__(**kwargs)
        self.db = db

    def process_IN_DELETE(self, event):
        self.db.delete_file(event.pathname)
        self.db.write_log(event)

    def process_IN_CREATE(self, event):
        self.db.create_new(event.pathname, event.dir, watched_dir)
        self.db.write_log(event)

    def process_IN_CLOSE_WRITE(self, event):
        self.db.put_file_revision(event.pathname)
        self.db.write_log(event)

    def process_IN_ATTRIB(self, event):
        self.db.put_file_revision(event.pathname)
        self.db.write_log(event)

    def process_IN_MOVED_TO(self, event):
        if hasattr(event, 'src_pathname'):
            self.db.move(event.pathname, watched_dir, event.src_pathname)
            self.db.write_log(event)
        else:
            self.db.move(event.pathname, watched_dir)
            self.db.write_log(event)


    # def process_default(self, event):
    #     print event
    #     self.db.write_log(event)
    #     # self.db.put_file_revision(event)


pyinotify.AsyncNotifier(wm, EventHandler(database))
wm.add_watch(watched_dir, mask, rec=True, auto_add=True)

asyncore.loop()