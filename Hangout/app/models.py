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
    

# no need for site.admin.register
