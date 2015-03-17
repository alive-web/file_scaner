import argparse
import asyncore
import pyinotify
from datetime import datetime
# from shutil import copyfile

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path',  type=str, default="/tmp",  help='path to scan directory')
args = parser.parse_args()

watched_dir = args.path
wm = pyinotify.WatchManager()

def write_log_in_db():
    # This function will accept one argument "event" and will record in db
    pass

def create_copy():
    # This function will accept one argument "path to file" and will record reserve copy file in db
    pass

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        print datetime.now(), "Creating:", event.pathname
        if event.dir:
            # restart loop
            pass

    def process_IN_DELETE(self, event):
        # copyfile(event.pathname, event.pathname+str(datetime.now()))
        print datetime.now(), "Removing:", event.pathname

    def process_IN_CLOSE_WRITE(self, event):
        print datetime.now(), "saving:", event.pathname

    def process_IN_ATTRIB(self, event):
        print datetime.now(), "changing permission:", event.pathname

notifier = pyinotify.AsyncNotifier(wm, EventHandler())
wdd = wm.add_watch(watched_dir, pyinotify.ALL_EVENTS, rec=True)

asyncore.loop()