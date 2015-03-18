import config
from datetime import datetime
from pymongo import MongoClient


class DataBase():
    def __init__(self):
        pass

    client = MongoClient(config.DB_HOST, config.DB_PORT)
    db = client.file_scaner
    events = db.events

    def write_log(self, event):
        action = {
            'date': datetime.now(),
            'event': event.maskname,
            'path_name': event.pathname
        }
        self.events.insert(action)

    def put_file_revision(self):
        # This method will accept one argument "path to file" and will record reserve copy file in db
        pass