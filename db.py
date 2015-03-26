import os
import config
import hashlib
from datetime import datetime
from mongoengine import connect
from models import Events, FileSystem


def write_fields(document, previous_version):
    previous_version.update(set__has_next=True)
    document.version = previous_version.version + 1
    document.previous_version = previous_version
    document.save()


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
        this_document = FileSystem.objects(path_name=event.pathname).order_by("-version").first()
        action.document = this_document
        action.save()

    def put_file_revision(self, pathname):
        if os.path.exists(pathname):
            st = os.stat(pathname)
            previous_version = FileSystem.objects(path_name=pathname).order_by("-version").first()
            with open(pathname, 'rb') as this_file:
                md5_sum = hashlib.md5(this_file.read()).hexdigest()
            document = FileSystem(path_name=pathname)
            if md5_sum != previous_version.hash_sum:
                with open(pathname, 'rb') as this_file:
                    document.body.put(this_file)
                document.hash_sum = md5_sum
                document.permissions = st.st_mode
                write_fields(document, previous_version)
            if previous_version.permissions != st.st_mode:
                document.permissions = st.st_mode
                write_fields(document, previous_version)

    def create_new(self, pathname, is_dir, watched_dir):
        if not FileSystem.objects(path_name=pathname):
            document = FileSystem(path_name=pathname, is_dir=is_dir)
            document.permissions = os.stat(pathname).st_mode
            path_parent = os.path.split(pathname)[0]
            if path_parent != watched_dir:
                parent = FileSystem.objects(path_name=path_parent).order_by("-version").first()
                document.parent = parent
            document.date = datetime.fromtimestamp(os.path.getmtime(pathname))
            if not is_dir and os.path.exists(pathname):
                with open(pathname, 'rb') as this_file:
                    document.body.put(this_file)
                    md5_sum = hashlib.md5(this_file.read()).hexdigest()
                document.hash_sum = md5_sum
            document.save()

    def delete_file(self, pathname):
        previous_version = FileSystem.objects(path_name=pathname).order_by("-version").first()
        document = FileSystem(path_name=pathname, is_del=True)
        write_fields(document, previous_version)

    def move(self, pathname, watched_dir, src_pathname=None):
        document = FileSystem(path_name=pathname)
        path_parent = os.path.split(pathname)[0]
        document.permissions = os.stat(pathname).st_mode
        if watched_dir != path_parent:
            document.parent = FileSystem.objects(path_name=path_parent).order_by("-version").first()
        if src_pathname:
            previous_version = FileSystem.objects(path_name=src_pathname).order_by("-version").first()
            previous_version.update(set__has_next=True)
            document.version = previous_version.version + 1
            document.previous_version = previous_version
        check = FileSystem.objects(path_name=pathname).order_by("-version").first()
        if check:
            check.has_next = True
            check.save()
        document.save()

    def get_tree(self, directory):
        path_to_file = FileSystem.objects(path_name__startswith=directory, has_next=False)
        return path_to_file

a = DataBase()
a.get_tree("/home/plevytskyi/test_scan")