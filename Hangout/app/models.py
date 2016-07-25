from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
import django.utils.timezone as timezone

#------------------  Tag  -------------------#

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


#--------------  application  ---------------#

APPLICATION_TYPE_MEMBER = 1
APPLICATION_TYPE_ADMIN = 2
APPLICATION_TYPE = (
    (APPLICATION_TYPE_MEMBER, 'member'),
    (APPLICATION_TYPE_ADMIN, 'admin'),
)
class Application(models.Model):
    """application to become member/admin of a activity"""
    applicant = models.ForeignKey('User', related_name='applications')
    application_type = models.IntegerField(default=1, choices=APPLICATION_TYPE)
    activity = models.ForeignKey('Activity', related_name='applications')
    intro = models.CharField(max_length=200, default='no introduction')
    time = models.DateTimeField(auto_now_add=True)


#----------------  Message  -----------------#

class Message(models.Model):
    from_user = models.ForeignKey('User', related_name='sent_messages')
    to_user = models.ForeignKey('User', related_name='messages')
    content = models.CharField(max_length=1000)
    read = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)


#-----------------  Notice  -----------------#

class Notice(models.Model):
    activity = models.ForeignKey('Activity', related_name='notices', blank=True)
    from_user = models.ForeignKey('User', related_name='sent_notice')
    content = models.CharField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True)


#----------------  Activity  ----------------#

ACTIVITY_STATES_OPEN = 0
ACTIVITY_STATES_CLOSED = 1
ACTIVITY_STATES_ENDED = 2
ACTIVITY_STATES_STARTED = 3

ACTIVITY_STATES = (
    (ACTIVITY_STATES_OPEN, 'open'),
    (ACTIVITY_STATES_CLOSED, 'closed'),
    # (ACTIVITY_STATES_STARTED, 'started'),
    (ACTIVITY_STATES_ENDED, 'ended'),
)

class Activity(models.Model):
### basic information 
    name = models.CharField(max_length=100)
    intro = models.CharField(max_length=1000)
    tags = models.ManyToManyField(Tag, related_name='acts')
    cost = models.FloatField(default=0.0)
    location = models.CharField(max_length=100, default='pending')
    time = models.DateTimeField(auto_now_add=True)

    state = models.IntegerField(default=0)
    organizer = models.ForeignKey('User', related_name='org_acts')

    create_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name


#------------------  User  ------------------#

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')
        if not kwargs.get('name'):
            raise ValueError('Users must have a valid username.')
        user = self.model(
            email=self.normalize_email(email), name=kwargs.get('name')
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password, **kwargs)
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser):
### basic info
    name = models.CharField(max_length=100)
    cellphone = models.CharField(max_length=20)
    score = models.FloatField(default=0.0)
    portrait = models.ImageField()
    email = models.EmailField(unique=True)
    intro = models.CharField(default='', max_length=200)
    state = models.CharField(default='', max_length=50)
### org_acts: has defined in Activity
    # apply_acts = models.ManyToManyField(Activity, related_name='applicants')
    join_acts = models.ManyToManyField(Activity, related_name='members')
    admin_acts = models.ManyToManyField(Activity, related_name='admins')
    coll_acts = models.ManyToManyField(Activity, related_name='collected')
    # everyday divide into 4 time period, stored with 0/1, so 4*7 = 28 bit used totally
    fix_times = models.IntegerField(default=0)
    tmp_times = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, related_name='users')
### messages: has defined in Message
    # Usage see: http://charlesleifer.com/blog/self-referencing-many-many-through/
    follow = models.ManyToManyField('self', through='Relationship',
                                     symmetrical=False,
                                     related_name='followed')
    is_admin = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    def __str__(self):
        return self.email


#--------------  Relationshio  --------------#

RELATIONSHIP_FOLLOWING = 1
RELATIONSHIP_BLOCKED = 2
RELATIONSHIP_STATUSES = (
    (RELATIONSHIP_FOLLOWING, 'Following'),
    (RELATIONSHIP_BLOCKED, 'Blocked'),
)
class Relationship(models.Model):
    from_user = models.ForeignKey(User, related_name='from_people')
    to_user = models.ForeignKey(User, related_name='to_people')
    status = models.IntegerField(choices=RELATIONSHIP_STATUSES)
