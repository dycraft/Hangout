# coding=utf-8
from .models import *
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods

import json

from .serializer import *
from .utilities import send_message, authentication
from .tag import get_tag

'''
ger_user:
    get user info by id

GET param
---------------------------------------------------------------------
| param     | introduction                   | default              |
|===================================================================|
| id        | id of user                     | REQUIRED             |
|===================================================================|    

returns:
    'state_code'
    'user_info' -- when (state_code == 0)

'''
def get_user(request, id):
    ret = dict()

    try:
        user = User.objects.get(id=id)
        ret['user_info'] = user_serialize(user)
        ret['state_code'] = 0
    except User.DoesNotExist:
        ret['state_code'] = 2
    return HttpResponse(json.dumps(ret), content_type='application/json')

'''
login_detail:
    get user detail that is currently logged in

No params required

returns:
    'state_code'
    'user_info' -- when (state_code == 0)

'''
def login_detail(request):
    ret = dict()
    user = request.user
    if not user.is_authenticated():
        ret['state_code'] = 1
    else: 
        ret['user_info'] = user_serialize(user)
        ret['state_code'] = 0
    return HttpResponse(json.dumps(ret), content_type='application/json')


'''
update_user:
    update user info(only by admin and user itself)

POST params
---------------------------------------------------------------------
| param     | introduction                   | default              |
|===================================================================|
| email     | email of user                  | REQUIRED             |
| name      | name of user                   | No Default           |
| intro     | introduction of user           | No Default           |
| tags      | tags of act (delimited by ',') | ''                   |
| cellphone | cellphone of user              | No Default           |
| fix_times | fix times of user              | No Default           |
| tmp_times | temp times of user             | No Default           |
|===================================================================|

returns:
    'state_code'
    'user_info' -- when (state_code == 0)

'''
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
            ret['user_info'] = user_serialize(user, False)
        except User.DoesNotExist:
            ret['state_code'] = 2

    return HttpResponse(json.dumps(ret), content_type='application/json')


'''
update_portrait:
    update the portrait of a member



'''
def update_portrait(request):
    pass


'''
update_password:
    update user password(only by admin and user itself), automatically
    logout when succeeded

POST params
---------------------------------------------------------------------
| param     | introduction                   | default              |
|===================================================================|
| email     | email of user                  | REQUIRED             |
| password  | password of user               | REQUIRED             |
|===================================================================|

returns:
    'state_code'

'''
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

'''
update_user:
    delete user account(only admin and user itself)

POST params
---------------------------------------------------------------------
| param     | introduction                   | default              |
|===================================================================|
| email     | email of user                  | REQUIRED             |
|===================================================================|

returns:
    'state_code'

'''
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

'''
user_exist:
    check if a email is used

GET params
---------------------------------------------------------------------
| param     | introduction                   | default              |
|===================================================================|
| email     | email of user                  | REQUIRED             |
|===================================================================|

returns 
    'used'
'''
def user_exist(request, email):
    ret = dict()
    ret['used'] = (len(User.objects.filter(email=email)) > 0)

    return HttpResponse(json.dumps(ret), content_type='application/json')


'''
user_register:
    register a new user

POST params
---------------------------------------------------------------------
| param     | introduction                   | default              |
|===================================================================|
| email     | email of user                  | REQUIRED             |
| password  | password of user               | REQUIRED             |
| name      | name of user                   | 'anonymous'          |
| intro     | introduction of user           | ''                   |
| tags      | tags of act (delimited by ',') | ''                   |
| cellphone | cellphone of user              | ''                   |
| fix_times | fix times of user              | 0                    |
| portrait  | user portrait(not implemented) | not implemented      |
|===================================================================|

returns:
    'state_code'
    'user_info' -- when (state_code == 0 or state_code == 6)

'''
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
        # user_info['portrait'] = request.POST.get('portrait')
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
                user = User.objects.create_user(
                            user_info['email'], 
                            user_info['password'], 
                            name = user_info['name']
                        )
                # user.portrait = user_info['portrait']
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
            
'''
user_login:
    user login

POST params
---------------------------------------------------------------------
| param     | introduction                   | default              |
|===================================================================|
| email     | email of user                  | REQUIRED             |
| password  | password of user               | REQUIRED             |
|===================================================================|

returns:
    'state_code'
    'user_info' -- when (state_code == 0)

'''
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

'''
user_logout:
    user logout

No params required

returns:
    'state_code'

'''
def user_logout(request):
    ret = dict()
    if not request.user.is_authenticated():
        ret['state_code'] = 1
    else:
        logout(request)
        ret['state_code'] = 0
    return HttpResponse(json.dumps(ret), content_type='application/json')

'''
get_admin_activity:
    get activities that user has admin permission

GET

returns:
    'state_code'
    'admin_acts' -- when (state_code == 0)
'''
def get_admin_activity(request):
    ret = dict()
    r = authentication(request,require_authenticate=True)
    if not r['state_code'] == 0:
        ret['state_code'] = r['state_code']
    else:
        ret['admin_acts'] = []
        for act in request.user.admin_acts.all():
            ret['admin_acts'].append(activity_serialize(act))
    return HttpResponse(json.dumps(ret), content_type='application/json')

'''
get_admin_activity:
    get activities that user joins in.

GET

returns:
    'state_code'
    'join_acts' -- when (state_code == 0)
    'apply_acts_member'
    'apply_acts_admin'
'''
def get_join_activity(request):
    ret = dict()
    r = authentication(request,require_authenticate=True)
    if not r['state_code'] == 0:
        ret['state_code'] = r['state_code']
    else:
        ret['join_acts'] = []
        ret['apply_acts_member'] = []
        ret['apply_acts_admin'] = []
        for act in request.user.join_acts.all():
            ret['join_acts'].append(activity_serialize(act))
        for app in request.user.applications.filter(application_type=1):
            ret['apply_acts_member'].append(activity_serialize(app.activity))
        for app in request.user.applications.filter(application_type=2):
            ret['apply_acts_admin'].append(activity_serialize(app.activity))

    return HttpResponse(json.dumps(ret), content_type='application/json')

'''
apply_for_activity:
    apply activity permission (member/admin)

POST params
---------------------------------------------------------------------
| param     | introduction                   | default              |
|===================================================================|
| act_id    | id of activity                 | REQUIRED             |
| type      | 1 for member / 2 for admin     | 1                    |
| intro     | introduction of user itself    | 'no introduction'    |
|===================================================================|

returns:
    'state_code'

'''
@require_http_methods(['POST'])
def apply_for_activity(request):
    ret = dict()
    act_id = request.POST.get('act_id')
    if not request.user.is_authenticated():
        ret['state_code'] = 1
    elif not act_id:
        ret['state_code'] = 51
    elif not act_id in ['1', '2']:
        ret['state_code'] = 11
    else:
        act = Activity.objects.filter(id=act_id)
        app_type = request.POST.get('type', 1)
        intro = request.POST.get('intro', 'no introduction')
        if len(act) == 0:
           ret['state_code'] = 51
        elif len(act[0].applications.filter(
                        applicant_id=request.user.id, 
                        application_type=app_type)) > 0:
            ret['state_code'] = 53
        elif app_type == '1' and len(act[0].members.filter(id=request.user.id)) > 0:
            ret['state_code'] = 55
        elif app_type == '2' and len(act[0].admins.filter(id=request.user.id)) > 0:
            ret['state_code'] = 56
        elif app_type == '2' and len(act[0].members.filter(id=request.user.id)) == 0:
            ret['state_code'] = 54
        else:
            app = Application.objects.create(
                    applicant=request.user,
                    application_type=app_type,
                    activity=act[0],
                    intro=intro
                )
            app.save()

            request.user.save()
            ret['state_code'] = 0
    return HttpResponse(json.dumps(ret), content_type='application/json')

'''
quit_activity:
    Quit activity. User is Deleted from 'applicants', 'admins'
    and 'members'. Applications are also deleted.

POST params
---------------------------------------------------------------------
| param     | introduction                   | default              |
|===================================================================|
| act_id    | id of activity                 | REQUIRED             |
|===================================================================|

returns:
    'state_code'

'''
@require_http_methods(['POST'])
def quit_activity(request):
    ret = dict()
    act_id = request.POST.get('act_id')
    user = request.user
    if not user.is_authenticated():
        ret['state_code'] = 1
    elif not act_id:
        ret['state_code'] = 51
    else:
        act = Activity.objects.filter(id=act_id)
        if len(act) == 0:
            ret['state_code'] = 52
        else:
            act[0].applicants.remove(user)
            act[0].admins.remove(user)
            act[0].members.remove(user)
            act[0].applications.filter(applicant_id=user.id).delete()
            ret['state_code'] = 0
    return HttpResponse(json.dumps(ret), content_type='application/json')

'''
get_message:
    get message list of a user

POST params
---------------------------------------------------------------------
| param     | introduction                   | default              |
|===================================================================|
| id        | id of user                     | REQUIRED             |
| setting   | 0: all messages                | 0                    |
|           | 1: all messages sent by user   |                      |
|           | 2: all messages sent to user   |                      |
|           | 3: all unread messages         |                      |
|===================================================================|

returns:
    'state_code'
    'messages' -- when (state_code = 0)
'''
@require_http_methods(['POST'])
def get_message(request):
    ret = dict()

    setting = int(request.POST.get('setting', 0))

    r = authentication(request,
                        required_param=['id'],
                        require_authenticate=True,
                        require_model=True,
                        require_permission=True,
                        model=User,
                        keytype='id')
    if not r['state_code'] == 0:
        ret['state_code'] = r['state_code']
    else:
        user = r['record']
        ret['messages'] = []
        ret['state_code'] = 0
        if setting == 0:
            # for m in user.sent_messages.all():
            #     ret['messages'].append(message_serialize(m))
            # for m in user.messages.all():
            #     ret['messages'].append(message_serialize(m))
            msgs = sorted(user.sent_messages.all() | user.messages.all(), key=lambda x:x.time)
            for m in msgs:
                ret['messages'].append(message_serialize(m))
        elif setting == 1:
            for x in user.sent_messages.all():
                ret['messages'].append(message_serialize(m))
        elif setting == 2:
            for m in user.messages.all():
                ret['messages'].append(message_serialize(m))
        elif setting == 3:
            for m in user.messages.filter(read=False):
                ret['messages'].append(message_serialize(m))
    return HttpResponse(json.dumps(ret), content_type='application/json')

'''
set_message_state:
    set message read state

GET param
---------------------------------------------------------------------
| param     | introduction                   | default              |
|===================================================================|
| id        | id of message                  | REQUIRED             |
| state     | state of msg user want to set  | REQUIRED             |
|===================================================================|

returns:
    'state_code'
'''
def set_message_state(request, id, state):
    ret = dict()
    msg = Message.objects.filter(id=id)
    if len(msg) == 0: 
        ret['state_code'] = 31
    else:
        msg = msg[0]
        if not (request.user.is_admin == True or msg.to_user.id == request.user.id):
            ret['state_code'] = 3
        else:
            if state == '1':
                msg.read = True            
                ret['state_code'] = 0
                msg.save()
            elif state == '0':
                msg.read = False
                ret['state_code'] = 0
                msg.save()
            else:
                ret['state_code'] = 32
    return HttpResponse(json.dumps(ret), content_type='application/json')


'''
send_message_post:
    send message

POST param
---------------------------------------------------------------------
| param     | introduction                   | default              |
|===================================================================|
| id        | id of user(send to)            | REQUIRED             |
| content   | content of message             | REQUIRED             |
|===================================================================|

'''
def send_message_post(request):
    ret = dict()
    r = authentication(request, 
                     required_param=['id','content'],
                     require_authenticate=True,
                     require_model=True,
                     model=User,
                     keytype='id')
    if r['state_code'] == 0:
        to_user = r['record']
        content = r['param']['content']
        send_message(request.user, to_user, content)
        ret['state_code'] = 0
    else:
        ret['state_code'] = r['state_code']
    return HttpResponse(json.dumps(ret), content_type='application/json')



'''
follow:
    follow another user

POST param
---------------------------------------------------------------------
| param     | introduction                   | default              |
|===================================================================|
| id        | id of user(to be followed)     | REQUIRED             |
|===================================================================|

returns:
    'state_code'
'''
@require_http_methods(['POST'])
def follow(request):
    ret = dict()
    r = authentication(request, 
                 required_param=['id'],
                 require_authenticate=True,
                 require_model=True,
                 model=User,
                 keytype='id')
    if not r['state_code'] == 0:
        ret['state_code'] = r['state_code']
    elif r['record'].id == request.user.id:
        ret['state_code'] = 12
    else:
        r, c = Relationship.objects.get_or_create(
            from_user=request.user,
            to_user=r['record'])
        if not c == True:
            ret['state_code'] = 13
        else:
            ret['state_code'] = 0
    return HttpResponse(json.dumps(ret), content_type='application/json')



'''
unfollow:
    unfollow another user

POST param
---------------------------------------------------------------------
| param     | introduction                   | default              |
|===================================================================|
| id        | id of user(followed)           | REQUIRED             |
|===================================================================|

returns:
    'state_code'
'''
@require_http_methods(['POST'])
def unfollow(request):
    ret = dict()
    r = authentication(request, 
                 required_param=['id'],
                 require_authenticate=True,
                 require_model=True,
                 model=User,
                 keytype='id')
    if not r['state_code'] == 0:
        ret['state_code'] = r['state_code']
    elif r['record'].id == request.user.id:
        ret['state_code'] = 12
    else:
        r = Relationship.objects.filter(
            from_user=request.user,
            to_user=r['record'])
        if len(r) == 0:
            ret['state_code'] = 14
        else:
            r.delete()
            ret['state_code'] = 0
    return HttpResponse(json.dumps(ret), content_type='application/json')


'''
check_following:
    check all following users with their state

no params required

returns:
    'state_code'
    'following' -- [{'id': id, 'name':name, 'state': state}]
'''
def check_following(request):
    ret = dict()
    r = authentication(request, 
                 required_param=[],
                 require_authenticate=True)
    if not r['state_code'] == 0:
        ret['state_code'] = r['state_code']
    else:
        ret['following'] = []
        for r in request.user.follow.filter(to_people__from_user=request.user):
            ret['following'].append({'id': r.id, 'name': r.name})
        ret['state_code'] = 0
    return HttpResponse(json.dumps(ret), content_type='application/json')
    


'''
check_follower:
    check all follower users

no params required

returns:
    'state_code'
    'follower' -- [{'id': id, 'name':name}]
'''
def check_follower(request):
    ret = dict()
    r = authentication(request, 
                 required_param=[],
                 require_authenticate=True)
    if not r['state_code'] == 0:
        ret['state_code'] = r['state_code']
    else:
        ret['follower'] = []
        for r in request.user.followed.all():
            ret['follower'].append({'id': r.id, 'name': r.name})
        ret['state_code'] = 0
    return HttpResponse(json.dumps(ret), content_type='application/json')
    



















#-------------------------------------------------------------------

def testauthentication(request):
    ret = dict()
    r = authentication(request, 
                     required_param=['id'],
                     require_authenticate=True,
                     require_model=True,
                     # require_permission=True,
                     model=Activity,
                     keytype='id')
    if r['state_code']==0:
        ret['info'] = activity_serialize(r['record'])
    else:
        ret['state_code'] = r['state_code']
    return HttpResponse(json.dumps(ret), content_type='application/json')


