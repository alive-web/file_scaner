from datetime import datetime
from mongoengine import Document, fields


class Events(Document):
    date = fields.DateTimeField(default=datetime.now)
    event = fields.StringField(max_length=30)
    path_name = fields.StringField(max_length=200)