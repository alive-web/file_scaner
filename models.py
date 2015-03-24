from datetime import datetime
from mongoengine import Document, fields


class Events(Document):
    date = fields.DateTimeField(default=datetime.now)
    event = fields.StringField(max_length=30)
    path_name = fields.StringField(max_length=200)
    src_path_name = fields.StringField(max_length=200)


class FileSystem(Document):
    path_name = fields.StringField()
    parent = fields.StringField()
    permissions = fields.IntField()
    version = fields.IntField(default=1)
    date = fields.DateTimeField(default=datetime.now)
    body = fields.FileField()
    is_dir = fields.BooleanField(default=False)
    is_del = fields.BooleanField(default=False)