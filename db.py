import config
from models import Events
from mongoengine import connect


class DataBase():
    def __init__(self):
        connect(
            config.DB_NAME,
            host=config.DB_HOST,
            port=config.DB_PORT,
            username=config.DB_USERNAME,
            password=config.DB_PASSWORD
        )

    def write_log(self, event):
        action = Events(event=event.maskname, path_name=event.pathname)
        action.save()

    def put_file_revision(self):
        # This method will accept one argument "path to file" and will record reserve copy file in db
        pass