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
        if str(event.maskname) != "IN_CREATE|IN_ISDIR" and str(event.maskname) != "IN_DELETE" and str(
                event.maskname) != "IN_IGNORED":
            this_file = open(event.pathname, 'rb')
            action.file.put(this_file)
        action.save()

    def put_file_revision(self, event):
        pass
