import os
import datetime
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

    def put_file_revision(self, pathname, path):
        test_doc = FileSystem.objects(path_name=pathname).order_by("-version").first()
        st = os.stat(pathname)
        if os.path.exists(pathname):
            # and test_doc.permissions != st.st_mode

            document = FileSystem(path_name=pathname, parent=path)
            document.permissions = st.st_mode
            with open(pathname, 'rb') as this_file:
                document.body.put(this_file)
            versions = FileSystem.objects(path_name=pathname).distinct("version")
            if len(versions) != 0:
                document.version = max(versions) + 1
            document.save()

    def create_new(self, pathname, path, is_dir, *args):
        if not FileSystem.objects(path_name=pathname):
            document = FileSystem(path_name=pathname, parent=path, is_dir=is_dir)
            document.permissions = os.stat(pathname).st_mode
            if args:
                document.date = args[0]
            if not is_dir and os.path.exists(pathname):
                with open(pathname, 'rb') as this_file:
                    document.body.put(this_file)
            document.save()

    def delete_file(self, pathname, path, is_dir):
        document = FileSystem(path_name=pathname, parent=path, is_dir=is_dir, is_del=True)
        versions = FileSystem.objects(path_name=pathname).distinct("version")
        if len(versions) != 0:
            document.version = max(versions) + 1
        document.save()