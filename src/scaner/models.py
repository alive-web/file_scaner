from datetime import datetime
from mongoengine import Document, fields


class FileSystem(Document):
    path_name = fields.StringField()
    parent = fields.ReferenceField("self")
    permissions = fields.IntField()
    previous_version = fields.ReferenceField("self")
    has_next = fields.BooleanField(default=False)
    hash_sum = fields.StringField(max_length=60)
    version = fields.IntField(default=1)
    date = fields.DateTimeField(default=datetime.now)
    body = fields.FileField()
    is_dir = fields.BooleanField(default=False)
    is_del = fields.BooleanField(default=False)

    def write_fields(self, previous_version):
        previous_version.update(set__has_next=True)
        self.version = previous_version.version + 1
        self.previous_version = previous_version
        self.save()

    def __str__(self):
        return '%s' % self.path_name


class Events(Document):
    date = fields.DateTimeField(default=datetime.now)
    event = fields.StringField(max_length=30)
    path_name = fields.StringField(max_length=200)
    document = fields.ReferenceField(FileSystem)

    def __str__(self):
        return "(%s) pathname %s" % (self.event, self.path_name)