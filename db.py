from datetime import datetime
from pymongo import MongoClient

class DataBase():
    client = MongoClient('localhost', 27017)
    db = client.file_scaner
    events = db.events

    def write_log(self, event):
        print event
        action = {
            'date': datetime.now(),
            'event': event.maskname,
            'path_name': event.pathname
        }
        self.events.insert(action)

    def create_copy():
        # This method will accept one argument "path to file" and will record reserve copy file in db
        pass