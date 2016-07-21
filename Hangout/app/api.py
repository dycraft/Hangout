from django.shortcuts import render
from django.http import HttpResponse


import json

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
    pass
