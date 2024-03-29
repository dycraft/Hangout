# coding=utf-8
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .tag import *
from .serializer import *
from .models import *
from .utilities import *
from .message_templates import *
from .feature import update_feature, feature_length

import json
import datetime

'''
has_permission:
	Utility function, check if a user have the permission to modify a act

params
	user
	act
'''
def has_permission(user, act):
	if user.is_admin == True:
		return True
	elif len(act.admins.filter(id=user.id)) == 0:
		return False
	else:
		return True


'''
create_activity:
	Create an activity, user that is currently logged in will become
	the organizer and an admin automatically

POST params
---------------------------------------------------------------------
| param     | introduction                   | default              |
|===================================================================|
| name      | name of act                    | 'untitled'           |
| intro     | introduction of act            | 'No intro available' |
| tags      | tags of act (delimited by ',') | ''                   |
| cost      | estimated cost of act          | 0                    |
| location  | location of act                | ''            |
| time      | time(not implemented yet)      | datetime.now()       |
| limit     | limit of number of members     | 10000                |
|===================================================================|
'''
@require_http_methods(['POST'])
def create_activity(request):
	ret = dict()
	if not request.user.is_authenticated():
		ret['state_code'] = 1
	else:
		act_info = dict()
		act_info['name'] = request.POST.get('name', 'untitled')
		act_info['intro'] = request.POST.get('intro', 'No intro available')
		act_info['tags'] = request.POST.get('tag', '').split(',')
		act_info['cost'] = float(request.POST.get('cost', 0))
		act_info['location'] = request.POST.get('location', '')
		act_info['limit'] = request.POST.get('limit', 10000)
		act_info['organizer'] = request.user.email
		act = Activity.objects.create(
				name=act_info['name'],
				intro=act_info['intro'],
				cost=act_info['cost'],
				organizer_id=request.user.id,
				location=act_info['location'],
				state = act_info['limit'] << 2,
			)
		act.admins.add(request.user)
		act.members.add(request.user)
		for t in act_info['tags']:
			if not t.strip() == '':
				act.tags.add(get_tag(t.strip()))

		act.save()
		act.update_feature()
		ret['state_code'] = 0


	return HttpResponse(json.dumps(ret), content_type='application/json')


'''
get_activity_detail:
	get detail of an activity, if 'detailed' param is provided and
	equals to 'True', it will return a detailed version of info,
	including 'applicants', 'members', 'admins' and 'collected'

POST params
---------------------------------------------------------------------
| param     | introduction                   | default              |
|===================================================================|
| id        | id of act                      | REQUIRED             |
| detailed  | get a detailed info            | 'False'              |
|===================================================================|
'''
def get_activity_detail(request, id):
	ret = dict()
	try:
		act = Activity.objects.get(id=id)
		ret['act_info'] = activity_serialize(act)
		ret['state_code'] = 0
	except Activity.DoesNotExist:
		ret['state_code'] = 52
	return HttpResponse(json.dumps(ret), content_type='application/json')


'''
update_activity:
	Update activity info. Similar to create_activity

POST params
---------------------------------------------------------------------
| param     | introduction                   | default              |
|===================================================================|
| id        | id of act                      | REQUIRED             |
| name      | name of act                    | 'untitled'           |
| intro     | introduction of act            | 'No intro available' |
| tags      | tags of act (delimited by ',') | ''                   |
| cost      | estimated cost of act          | 0                    |
| location  | location of act                | 'pending'            |
| time      | time of activity               | datetime.now()       |
| end_time  | end_time of activity           | datetime.now()       |
|===================================================================|
'''
@require_http_methods(['POST'])
def update_activity(request):
	ret = dict()

	r = authentication(request,
						required_param=['id'],
						require_authenticate=True,
						require_model=True,
						model=Activity,
						keytype='id')

	if not r['state_code'] == 0:
		ret['state_code'] = r['state_code']
	else:
		act = r['record']
		if not has_permission(request.user, act):
			ret['state_code'] = 3
		else:

			items = request.POST.items()
			keys = [k for k, v in items]

			info = dict()
			act.name = request.POST.get('name', act.name)
			act.intro = request.POST.get('intro', act.intro)
			act.cost = float(request.POST.get('cost', act.cost))
			act.location = request.POST.get('location', act.location)
			act.state = int(request.POST.get('amount', act.state >> 2)) << 2 + act.state % 4

			if 'tags' in keys:
				tags = [t.strip() for t in request.POST.get('tags').split(',')]
				for tag in act.tags.all():
					act.tags.remove(tag)
				for tag in tags:
					if not tag == '':
						act.tags.add(get_tag(tag))

			act.update_feature()

			### update time
			f = '%Y-%m-%d %H'
			time_str = request.POST.get('time')
			if time_str:
				act.time = datetime.datetime.strptime(time_str, f)

			end_time_str = request.POST.get('end_time')
			if end_time_str:
				act.end_time = datetime.datetime.strptime(end_time_str, f)

			act.save()
			ret['state_code'] = 0
			ret['act_info'] = activity_serialize(act)

			send_update_activity_message(request.user, act)

	return HttpResponse(json.dumps(ret), content_type='application/json')


'''
get_recommended_time:
	get a recomended time of an act based on fix_time of user


'''
def get_recommended_time(request, id):
	ret = dict()

	act = Activity.objects.filter(id=id)
	if len(act) == 0:
		ret['state_code'] = 52
	else:
		ret['state_code'] = 0
		act = act[0]
		ret['result'] = []
		mem = 0
		for x in range(0, 28):
			ret['result'].append(0)

		for u in act.members.all():
			t = u.fix_times
			temp = 1 << 27
			for x in range(0, 28):
				# mem = mem + 1
				if (t & temp) > 0:
					ret['result'][x] += 1
				temp = temp >> 1
		mem = feature_length(ret['result'])
		for x in range(0, 28):
			ret['result'][x] = ret['result'][x] / mem
	return HttpResponse(json.dumps(ret), content_type='application/json')


'''
change_act_state:
	change act state

POST params
---------------------------------------------------------------------
| param     | introduction                   | default              |
|===================================================================|
| id        | id of an activity              | REQUIRED             |
| state     | state of an activity           | REQUIRED             |
|===================================================================|


'''
def change_act_state(request):
	ret = dict()

	r = authentication(request,
						required_param=['id', 'state'],
						require_authenticate=True,
						require_model=True,
						model=Activity,
						keytype='id')

	if not r['state_code'] == 0:
		ret['state_code'] = r['state_code']
	else:
		act = r['record']
		state = r['params']['state']
		if not has_permission(request.user, act):
			ret['state_code'] = 3
		elif not str(state) in ['0', '1', '2']:
			ret['state_code'] = 11
		else:
			act.state = state
			act.save()
			ret['state_code'] = 0
	return HttpResponse(json.dumps(ret), content_type='application/json')

'''
get_applications:
	get applications of an activity

POST params
---------------------------------------------------------------------
| param     | introduction                   | default              |
|===================================================================|
| act_id    | id of an activity              | REQUIRED             |
|===================================================================|

returns:
	'state_code'
	'applications' -- when (state_code == 0)
'''
@require_http_methods(['POST'])
def get_applications(request):
	ret = dict()
	act_id = request.POST.get('act_id')
	if not request.user.is_authenticated():
		ret['state_code'] = 1
	elif not act_id:
		ret['state_code'] = 51
	else:
		act = Activity.objects.filter(id=act_id)
		if len(act) == 0:
			ret['state_code'] = 52
		elif has_permission(request.user, act[0]):
			ret['applications'] = []
			ret['state_code'] = 0
			for app in act[0].applications.all():
				ret['applications'].append(application_serialize(app))
		else:
			ret['state_code'] = 3
	return HttpResponse(json.dumps(ret), content_type='application/json')

'''
promote:
	
id: id of activity
user_id: id of user 
'''
def promote(request):
	ret = dict()
	r = authentication(request,
					required_param=['id'],
					require_authenticate=True,
					require_model=True,
					model=Activity,
					keytype='id')
	if not r['state_code'] == 0:
		ret['state_code'] = r['state_code']
	else:
		act = r['record']
		user_id = request.POST.get('user_id')
		user = User.objects.filter(id=user_id)
		if len(user) == 0:
			ret['state_code'] = 2
		else:
			user = user[0]
			if len(act.members.filter(id=user.id)) > 0 and len(act.admins.filter(id=user.id)) == 0 :
				act.admins.add(user)
				act.members.remove(user)
			ret['state_code'] = 0
	return HttpResponse(json.dumps(ret), content_type='application/json')

'''
kick_out:

id: id of activity
user_id: id of user 
'''
def kick_out(request):
	ret = dict()
	r = authentication(request,
					required_param=['id'],
					require_authenticate=True,
					require_model=True,
					model=Activity,
					keytype='id')
	if not r['state_code'] == 0:
		ret['state_code'] = r['state_code']
	else:
		act = r['record']
		user_id = request.POST.get('user_id')
		user = User.objects.filter(id=user_id)
		if len(user) == 0:
			ret['state_code'] = 2
		else:
			user = user[0]
			if len(act.members.filter(id=user.id)) > 0:
				act.admins.remove(user)
				act.members.remove(user)
				ret['state_code'] = 0

				send_message(request.user,
						user,
						kicked_out(act.name,
									request.user.name,
									user.name),
						2,
						admin_id=request.user.id,
						act_id=act.id)

			else:
				ret['state_code'] = 54
	return HttpResponse(json.dumps(ret), content_type='application/json')


'''
reply_application:
	reply an application of an activity (granted/refused)

POST params
---------------------------------------------------------------------
| param     | introduction                   | default              |
|===================================================================|
| user_id   | id of user                     | REQUIRED             |
| user_id   | id of user                     | REQUIRED             |
| reply     | 1 for granted / 0 for refused  | REQUIRED             |
|===================================================================|

returns:
	'state_code'
'''
def reply_application(request):
	ret = dict()
	user_id = request.POST.get('user_id')
	act_id = request.POST.get('act_id')
	reply = int(request.POST.get('reply'))
	if not request.user.is_authenticated():
		ret['state_code'] = 1
	elif not user_id or not act_id:
		ret['state_code'] = 101
	else:
		app = Application.objects.filter(activity__id=act_id ,applicant__id=user_id)
		if len(app) == 0:
			ret['state_code'] = 72
		elif has_permission(request.user, app[0].activity):
			app = app[0]
			if reply == 1:
				if app.application_type == 1:
					if len(app.activity.members.filter(id=app.applicant.id)) > 0:
						ret['state_code'] = 55
					else:
						app.activity.members.add(app.applicant)
						update_feature(app.activity, app.applicant)
						ret['state_code'] = 0
				elif app.application_type == 2:
					if len(app.activity.members.filter(id=app.applicant.id)) == 0:
						ret['state_code'] = 54
					elif len(app.activity.admins.filter(id=app.applicant.id)) > 0:
						ret['state_code'] = 56
					else:
						app.activity.admins.add(app.applicant)
						ret['state_code'] = 0

				if ret['state_code'] == 0:
					send_message(request.user,
						app.applicant,
						application_granted(app.applicant.name,
											app.application_type,
											app.activity.name,
											request.user.name),
						2,
						admin_id=request.user.id,
						act_id=app.activity.id)
				app.delete()

			if reply == 0:
				send_message(request.user,
					app.applicant,
					application_rejected(app.applicant.name,
										app.application_type,
										app.activity.name,
										request.user.name),
					2,
					admin_id=request.user.id,
					act_id=app.activity.id)

				app.delete()
				ret['state_code'] = 0
				ret['reply'] = 'refused'
		else:
			ret['state_code'] = 3
	return HttpResponse(json.dumps(ret), content_type='application/json')
