# coding=utf-8
from app.models import *
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

import json

from .models import User
from .serializer import user_serialize

# @user_permission(0)
### get user detail by user_id
def get_user(request, user_id):
    ret = dict()
    try:
        user = User.objects.get(id=user_id)
        ret = user_serialize(user)
    except User.DoesNotExist:
        ret['error'] = 'User does not exist'
    return HttpResponse(json.dumps(ret), content_type='application/json')

### get user detail that is currently logged in
def login_detail(request):
    ret = dict()
    user = request.user
    if not user.is_authenticated():
        ret['error'] = 'user not logged in'
    else: 
        return get_user(request, user.id)

### update user info(only by admin and user itself)
def update_user(request, user_id):
    ret = dict()
    if not request.user.is_authenticated():
        ret['error'] = 'user not logged in'
    elif (not str(request.user.id) == user_id) and (not request.user.is_admin == True):
        ret['error'] = 'permission denied'
    else:
        try:
            user = User.objects.get(id=user_id)
            
            editable_fields = [
                'name',
                'cellphone',
                'fix_times',
                'tmp_times',
            ]
            items = request.POST.items()
            for (k, v) in items:
                if k in editable_fields:
                    setattr(user, k, v)

            user.save()
            ret['response'] = 'success'

        except User.DoesNotExist:
            ret['error'] = 'user does not exist'

    return HttpResponse(json.dumps(ret), content_type='application/json')

### delete user account(only admin and user itself)
def delete_user(request, user_id):
    ret = dict()
    user = request.user
    if not user.is_authenticated():
        ret['error'] = 'user not logged in'
    elif not (user.id == user_id or user.is_admin == True):
        ret['error'] = 'permission denied'
    else:
        try:
            u = User.objects.get(id=user_id)
            u.delete()
            ret['response'] = 'success'
        except User.DoesNotExist:
            ret['error'] = 'User not exist'
    return HttpResponse(json.dumps(ret), content_type='application/json')

### register a new user
def user_register(request):
    ret = dict()
    if request.user.is_authenticated():
        ret['error'] = 'user already logged in'
    elif request.method == 'POST':
        ret['name'] = request.POST.get('name', 'anonymous')
        ret['password'] = request.POST.get('password', '')
        ret['portrait'] = request.POST.get('portrait')
        ret['email'] = request.POST.get('email', '')
        ret['fix_times'] = request.POST.get('fix_times', 0)
        ret['tags'] = request.POST.get('tags')
        if ret['email'] != '':
            try:
                User.objects.get(email=ret['email'])
                ret['error'] = 'repeated email address'
            except User.DoesNotExist:
                user = User.objects.create_user(ret['email'], ret['password'], name = ret['name'])
                user.portrait = ret['portrait']
                user.fix_times = ret['fix_times']
                user.tags = ret['tags']
                user.save()
                ret['response'] = 'success'
        else:
            ret['error'] = 'invalide email address'
    else:
        ret['error'] = 'need post'
    return HttpResponse(json.dumps(ret), content_type='application/json')
            
### user login
def user_login(request):
    ret = dict()
    if request.user.is_authenticated():
        ret['response'] = 'Already logged in'
    elif request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                name = user.name
                ret['response'] = 'success'
                ret['user_info'] = user_serialize(user)
            else:
                ret['error'] = 'freezed user'
        else:
            ret['email'] = email
            ret['password'] = password
            ret['error'] = 'wrong email/password'
    else:
        ret['error'] = 'need post'
    return HttpResponse(json.dumps(ret), content_type='application/json')

### user logout
def user_logout(request):
    ret = dict()
    if not request.user.is_authenticated():
        ret['error'] = 'not logged in yet'
    elif request.method == 'POST':
        logout(request)
        ret['response'] = 'success'
    else:
        ret['error'] = 'need post'
    return HttpResponse(json.dumps(ret), content_type='application/json')
