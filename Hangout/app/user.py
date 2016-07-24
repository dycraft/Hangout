# coding=utf-8
from .models import *
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods

import json

from .serializer import user_serialize
from .tag import get_tag

# @user_permission(0)
### get user detail by email
@require_http_methods(['POST'])
def get_user(request):
    ret = dict()
    email = request.POST.get('email')
    if not email:
        ret['state_code'] = 4
    else:
        try:
            user = User.objects.get(email=email)
            ret['user_info'] = user_serialize(user)
            ret['state_code'] = 0
        except User.DoesNotExist:
            ret['state_code'] = 2
    return HttpResponse(json.dumps(ret), content_type='application/json')

### get user detail that is currently logged in
def login_detail(request):
    ret = dict()
    user = request.user
    if not user.is_authenticated():
        ret['state_code'] = 1
    else: 
        ret['user_info'] = user_serialize(user)
        ret['state_code'] = 0
    return HttpResponse(json.dumps(ret), content_type='application/json')

### update user info(only by admin and user itself)
@require_http_methods(['POST'])
def update_user(request):
    ret = dict()
    email = request.POST.get('email')
    if not email:
        ret['state_code'] = 4
    elif not request.user.is_authenticated():
        ret['state_code'] = 1
    elif (not str(request.user.email) == email) and (not request.user.is_admin == True):
        ret['state_code'] = 3
    else:
        try:
            user = User.objects.get(email=email)
            
            ### update normal fields
            editable_fields = [
                'name',
                'cellphone',
                'intro',
                'fix_times',
                'tmp_times',
            ]
            items = request.POST.items()
            for (k, v) in items:
                if k in editable_fields:
                    setattr(user, k, v)
            ### update tags
            for tag in user.tags.all():
                user.tags.remove(tag)

            for tag in request.POST.get('tags', '').split(','):
                user.tags.add(get_tag(tag.strip()))

            user.save()

            ret['state_code'] = 0
            ret['user_info'] = user_serialize(user)
        except User.DoesNotExist:
            ret['state_code'] = 2

    return HttpResponse(json.dumps(ret), content_type='application/json')


@require_http_methods(['POST'])
def update_password(request):
    ret = dict()
    email = request.POST.get('email')
    if not email:
        ret['state_code'] = 4
    elif not request.user.is_authenticated():
        ret['state_code'] = 1
    elif not (str(request.user.email) == email or request.user.is_admin == True):
        ret['state_code'] = 3
    else:
        try:
            user = User.objects.get(email=email)
            password = request.POST.get('password')
            if not password:
                ret['state_code'] = 5
            else:
                user.set_password(password)
                ret['state_code'] = 0
                user.save()
        except User.DoesNotExist:
            ret['state_code'] = 2
    return HttpResponse(json.dumps(ret), content_type='application/json')

### delete user account(only admin and user itself)
@require_http_methods(['POST'])
def delete_user(request):
    ret = dict()
    email = request.POST.get('email') 
    user = request.user
    if not email:
        ret['state_code'] = 4
    elif not user.is_authenticated():
        ret['state_code'] = 1
    elif not (user.email == email or user.is_admin == True):
        ret['state_code'] = 3
    else:
        try:
            u = User.objects.get(email=email)
            u.delete()
            ret['state_code'] = 0
        except User.DoesNotExist:
            ret['state_code'] = 2
    return HttpResponse(json.dumps(ret), content_type='application/json')

### register a new user
@require_http_methods(['POST'])
def user_register(request):
    ret = dict()
    if request.user.is_authenticated():
        ret['state_code'] = 6
        ret['user_info'] = user_serialize(request.user)
    else:
        user_info = dict()
        user_info['name'] = request.POST.get('name', 'anonymous')
        user_info['password'] = request.POST.get('password', '')
        user_info['portrait'] = request.POST.get('portrait')
        user_info['email'] = request.POST.get('email', '')
        user_info['fix_times'] = request.POST.get('fix_times', 0)
        user_info['cellphone'] = request.POST.get('cellphone', '')
        user_info['intro'] = request.POST.get('intro', '')
        user_info['tags'] = [s.strip() for s in request.POST.get('tags', '').split(',')]
        if user_info['email'] != '' and user_info['password'] != '':
            try:
                User.objects.get(email=user_info['email'])
                user_info['state_code'] = 10
            except User.DoesNotExist:
                user = User.objects.create_user(user_info['email'], user_info['password'], name = user_info['name'])
                user.portrait = user_info['portrait']
                user.fix_times = user_info['fix_times']
                user.cellphone = user_info['cellphone']
                user.intro = user_info['intro']
                for s in user_info['tags']:
                    if not s == '':
                        try:
                            tag = Tag.objects.get(name=s)
                        except:
                            tag = Tag()
                            tag.name = s
                            tag.save()
                        user.tags.add(tag)
                user.save()
                ret['state_code'] = 0
                ret['user_info'] = user_serialize(user)
        else:
            ret['state_code'] = 9
    return HttpResponse(json.dumps(ret), content_type='application/json')
            
### user login
@require_http_methods(['POST'])
def user_login(request):
    ret = dict()
    if request.user.is_authenticated():
        ret['state_code'] = 6
        ret['user_info'] = user_serialize(request.user)
    else:
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                name = user.name
                ret['state_code'] = 0
                ret['user_info'] = user_serialize(user)
            else:
                ret['state_code'] = 7
        else:
            ret['state_code'] = 8
    return HttpResponse(json.dumps(ret), content_type='application/json')

### user logout
def user_logout(request):
    ret = dict()
    if not request.user.is_authenticated():
        ret['state_code'] = 1
    else:
        logout(request)
        ret['state_code'] = 0
    return HttpResponse(json.dumps(ret), content_type='application/json')
