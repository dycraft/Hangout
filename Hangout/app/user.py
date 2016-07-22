# coding=utf-8
from app.models import *
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
import json


# @user_permission(0)
def create_user(request):
    ret = dict()
    if request.method == 'POST':
        user = User()
        user.name = request.POST.get('name', '')
        ...
        ...
        ret['error'] = 'success'
        
    else:
        ret['error'] = 'need post'

    return HttpResponse(json.dumps(ret), content_type='application/json')

def get_user(request, user_id):
    ...

def update_user(request, user_id):
    ...

def delete_user(request, user_id):
    ...

def user_register(request):
    ret = dict()
    if request.method == 'POST':
        ret['name'] = request.POST.get('name', 'anonymous')
        ret['password'] = request.POST.get('password', '')
        ret['portrait'] = request.POST.get('portrait', '')
        ret['email'] = request.POST.get('email', '')
        ret['fix_times'] = request.POST.get('fix_times', '')
        ret['tags'] = request.POST.get('tags', '')
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
                ret['error'] = 'success'
        else:
            ret['error'] = 'invalide email address'
    else:
        ret['error'] = 'need post'
    return HttpResponse(json.dumps(ret), content_type='application/json')
            

def user_login(request):
    ret = dict()
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                name = user.name
                ret['name'] = name
            else:
                ret['error'] = 'freezed user'
        else:
            ret['error'] = 'wrong email/password'
    else:
        ret['error'] = 'need post'
    return HttpResponse(json.dumps(ret), content_type='application/json')

def user_logout(request):
    ret = dict()
    if request.method == 'POST':
        logout(request)
        ret['error'] = 'success'
    else:
        ret['error'] = 'need post'
    return HttpResponse(json.dumps(ret), content_type='application/json')
