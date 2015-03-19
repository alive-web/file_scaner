from mongoengine import *


class Events(Document):
    date = DateTimeField()
    event = StringField(max_length=30)
    path_name = StringField(max_length=200)