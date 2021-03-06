import os
import stat
import uuid
import config
import hashlib
from datetime import datetime
from mongoengine import connect
from hidden_document import is_hidden
from models import Events, FileSystem
from decorator import check_is_disabled


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
            this_document = FileSystem.objects(path_name=event.pathname).order_by("-version").first()
            if this_document:
                if not this_document.disabled:
                    action = Events(event=event.maskname, path_name=event.pathname)
                    action.document = this_document
                    action.save()

    @check_is_disabled
    def put_file_revision(self, pathname, previous_version=None):
        if os.path.exists(pathname):
            with open(pathname, 'rb') as this_file:
                md5_sum = hashlib.md5(this_file.read()).hexdigest()
            document = FileSystem(path_name=pathname, is_dir=os.path.isdir(pathname))
            if md5_sum != previous_version.hash_sum:
                with open(pathname, 'rb') as this_file:
                    document.body.put(this_file)
                document.hash_sum = md5_sum
                document.hidden = is_hidden(pathname)
                document.permissions = oct(stat.S_IMODE(os.lstat(pathname).st_mode))
                document.write_fields(previous_version)
            if previous_version.permissions != int(oct(stat.S_IMODE(os.lstat(pathname).st_mode))):
                document.hash_sum = md5_sum
                document.hidden = is_hidden(pathname)
                document.permissions = oct(stat.S_IMODE(os.lstat(pathname).st_mode))
                document.write_fields(previous_version)

    @check_is_disabled
    def create_new(self, pathname, watched_dir, *args):
        document = FileSystem.objects(path_name=pathname)
        if not document.count() and os.path.exists(pathname) or document.first().has_next:
            document = FileSystem(path_name=pathname, is_dir=os.path.isdir(pathname))
            document.permissions = oct(stat.S_IMODE(os.lstat(pathname).st_mode))
            document.hidden = is_hidden(pathname)
            path_parent = os.path.split(pathname)[0]
            if path_parent != watched_dir:
                parent = FileSystem.objects(path_name=path_parent, has_next=False).first()
                document.parent = parent
            document.date = datetime.fromtimestamp(os.path.getmtime(pathname))
            if not os.path.isdir(pathname) and os.path.exists(pathname):
                with open(pathname, 'rb') as this_file:
                    document.body.put(this_file)
                    md5_sum = hashlib.md5(this_file.read()).hexdigest()
                document.hash_sum = md5_sum
            document.key_for_all_versions = str(uuid.uuid4())
            document.save()

    @check_is_disabled
    def delete_file(self, pathname, previous_version=None):
        document = FileSystem(path_name=pathname, is_del=True, has_next=True, is_dir=os.path.isdir(pathname))
        document.write_fields(previous_version)

    @check_is_disabled
    def move(self, pathname, watched_dir, src_pathname=None, *args):
        document = FileSystem(path_name=pathname, is_dir=os.path.isdir(pathname))
        document.hidden = is_hidden(pathname)
        path_parent = os.path.split(pathname)[0]
        document.permissions = oct(stat.S_IMODE(os.lstat(pathname).st_mode))
        if watched_dir != path_parent:
            document.parent = FileSystem.objects(path_name=path_parent, has_next=False).first()
        previous_version_in_this_dir = FileSystem.objects(path_name=pathname, has_next=False).first()
        if previous_version_in_this_dir:
            if not previous_version_in_this_dir.has_next:
                if src_pathname:
                    src_file = FileSystem.objects(path_name=src_pathname, has_next=False).first()
                    src_file.has_next = True
                    src_file.save()
        elif src_pathname:
            previous_version = FileSystem.objects(path_name=src_pathname, has_next=False).first()
            document.hash_sum = previous_version.hash_sum
            document.permissions = previous_version.permissions
            parent = os.path.split(pathname)[0]
            document.write_fields(previous_version, parent)
        else:
            self.create_new(pathname, watched_dir)