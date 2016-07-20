from mongoengine import *
from django.http import HttpResponse
from datetime import datetime

# Create your models here.

class User(Document):
    name = StringField(required=True, max_length=100)
    password = StringField(required=True, max_length=100)
    cellphone = StringField(required=True)
    score = FloatField(default=0.0)
    portrait = ImageField()
    email = URLField()
    org_acts = ListField(IntField())
    join_acts = ListField(IntField())
    coll_acts = ListField(IntField())
    fix_times = ListField(IntField())
    tmp_times = ListField(IntField())
    tags = ListField(StringField(max_length=100))
    friends = ListField(IntField())
    messages = ListField(DictField())
    # from: IntField(), content: StringField()

class Activity(Document):
    name = StringField(required=True, max_length=100)
    intro = StringField(required=True)
    tags = ListField(required=True, StringField(max_length=100))
    cost = FloatField(default=0.0)
    organizer = IntField(required=True)
    admins = ListField(IntField())
    applicants = ListField(IntField())
    members = ListField(IntField())
    notices = ListField(DictField())
    # from: IntField(), content: StringField()
    messages = ListField(DictField())
    # from: IntField(), content: StringField()
    

# no need for site.admin.register
