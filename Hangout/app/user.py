# coding=utf-8
from app.models import *
from django.http import HttpResponse
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
