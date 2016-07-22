# coding=utf-8
from .models import *
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods

import json

from .serializer import user_serialize
from .tag import get_tag

# @user_permission(0)
### get user detail by user_id
@require_http_methods(['POST'])
def get_user(request):
    ret = dict()
    user_id = request.POST.get('user_id')
    if not user_id:
        ret['error'] = 'need user_id'
    else: 
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
        ret = user_serialize(user)
    return HttpResponse(json.dumps(ret), content_type='application/json')

### update user info(only by admin and user itself)
@require_http_methods(['POST'])
def update_user(request):
    ret = dict()
    user_id = request.POST.get('user_id')
    if not user_id:
        ret['error'] = 'need user_id'
    elif not request.user.is_authenticated():
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


@require_http_methods(['POST'])
def update_password(request):
    ret = dict()
    user_id = request.POST.get('user_id')
    if not user_id:
        ret['error'] = 'need user_id'
    elif not request.user.is_authenticated():
        ret['error'] = 'user not logged in'
    elif not (str(request.user.id) == user_id or request.user.is_admin == True):
        ret['error'] = 'permission denied'
    else:
        try:
            user = User.objects.get(id=user_id)
            password = request.POST.get('password')
            if not password:
                ret['error'] = 'must set a password'
            else:
                user.set_password(password)
                ret['response'] = 'success'
                user.save()
        except User.DoesNotExist:
            ret['error'] = 'User not exist'
    return HttpResponse(json.dumps(ret), content_type='application/json')

### delete user account(only admin and user itself)
@require_http_methods(['POST'])
def delete_user(request):
    ret = dict()
    user_id = request.POST.get('user_id')
    user = request.user
    if not user_id:
        ret['error'] = 'need user_id'
    elif not user.is_authenticated():
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
@require_http_methods(['POST'])
def user_register(request):
    ret = dict()
    if request.user.is_authenticated():
        ret['error'] = 'user already logged in'
    else:
        ret['name'] = request.POST.get('name', 'anonymous')
        ret['password'] = request.POST.get('password', '')
        ret['portrait'] = request.POST.get('portrait')
        ret['email'] = request.POST.get('email', '')
        ret['fix_times'] = request.POST.get('fix_times', 0)
        ret['tags'] = request.POST.get('tags', '').split('&&')
        if ret['email'] != '':
            try:
                User.objects.get(email=ret['email'])
                ret['error'] = 'repeated email address'
            except User.DoesNotExist:
                user = User.objects.create_user(ret['email'], ret['password'], name = ret['name'])
                user.portrait = ret['portrait']
                user.fix_times = ret['fix_times']
                for s in ret['tags']:
                    if not s == '':
                        try:
                            tag = Tag.objects.get(name=s)
                        except:
                            tag = Tag()
                            tag.name = s
                            tag.save()
                        user.tags.add(tag)
                user.save()
                ret['response'] = 'success'
        else:
            ret['error'] = 'invalide email address'
    return HttpResponse(json.dumps(ret), content_type='application/json')
            
### user login
@require_http_methods(['POST'])
def user_login(request):
    ret = dict()
    if request.user.is_authenticated():
        ret['response'] = 'Already logged in'
    else:
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
    return HttpResponse(json.dumps(ret), content_type='application/json')

### user logout
def user_logout(request):
    ret = dict()
    if not request.user.is_authenticated():
        ret['error'] = 'not logged in yet'
    else:
        logout(request)
        ret['response'] = 'success'
    return HttpResponse(json.dumps(ret), content_type='application/json')
