import config
from models import Events, FileSystem
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
        if hasattr(event, "src_pathname"):
            action.src_path_name = event.src_pathname
        action.save()

    def put_file_revision(self, event):
        if event.maskname == "IN_CREATE|IN_ISDIR":
            document = FileSystem(path_name=event.pathname, parent=event.path, is_dir=True)
            document.save()
        if event.maskname == "IN_CLOSE_WRITE":
            document = FileSystem(path_name=event.pathname, parent=event.path)
            this_file = open(event.pathname, 'rb')
            document.body.put(this_file)
            versions = FileSystem.objects(path_name=event.pathname).distinct("version")
            if len(versions) != 0:
                document.version = max(versions) + 1
            document.save()