# coding=utf-8
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .tag import *
from .serializer import *
from .models import *

import json

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
| location  | location of act                | 'pending'            |
| time      | time(not implemented yet)      | datetime.now()       |
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
		act_info['location'] = request.POST.get('location', 'pending')
		act_info['organizer'] = request.user.email
		act = Activity.objects.create(
				name=act_info['name'],
				intro=act_info['intro'],
				cost=act_info['cost'],
				organizer_id=request.user.id,
				location=act_info['location']
			)
		act.admins.add(request.user)
		for t in act_info['tags']:
			act.tags.add(get_tag(t.strip()))
		act.save()
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
| act_id    | id of act                      | REQUIRED             |
| detailed  | get a detailed info            | 'False'              |
|===================================================================|
'''
@require_http_methods(['POST'])
def get_activity_detail(request):
	ret = dict()
	act_id = request.POST.get('act_id')
	if not act_id:
		ret['state_code'] = 51
	else:
		try:
			act = Activity.objects.get(id=act_id)
			detailed = request.POST.get('detailed', 'False') == str(True)
			ret['act_info'] = activity_serialize(act, detailed)
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
| name      | name of act                    | 'untitled'           |
| intro     | introduction of act            | 'No intro available' |
| tags      | tags of act (delimited by ',') | ''                   |
| cost      | estimated cost of act          | 0                    |
| location  | location of act                | 'pending'            |
| time      | time of activity               | TO BE IMPLEMENTED    |
|===================================================================|
'''
@require_http_methods(['POST'])
def update_activity(request):
	ret = dict()
	act_id = request.POST.get('act_id')
	if not act_id:
		ret['state_code'] = 51
	elif not request.user.is_authenticated():
		ret['state_code'] = 1
	else:
		try:
			act = Activity.objects.get(id=act_id)

			if has_permission(request.user, act):
				ret['state_code'] = 3
			else:

				editable_fields = [
					'name',
					'intro',
					'cost',
					'location',
				]
				items = request.POST.items()
				keys = [k for k, v in items]
				for k,v in items:
					if k in editable_fields:
						setattr(act, k, v)
				
				if 'tags' in keys:
					tags = [t.strip() for t in request.POST.get('tags').split(',')]
					for tag in act.tags.all():
						act.tags.remove(tag)
					for tag in tags:
						act.tags.add(get_tag(tag))

				### update time --- to be implemented


				act.save()
				ret['state_code'] = 0
				ret['act_info'] = activity_serialize(act)

		except Activity.DoesNotExist:
			ret['state_code'] = 52
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
reply_application:
	reply an application of an activity (granted/refused)

POST params
---------------------------------------------------------------------
| param     | introduction                   | default              |
|===================================================================|
| app_id    | id of an application           | REQUIRED             |
| reply     | 1 for granted / 0 for refused  | REQUIRED             |
|===================================================================|

returns:
	'state_code'
'''
def reply_application(request):
	ret = dict()
	app_id = request.POST.get('app_id')
	reply = int(request.POST.get('reply'))
	if not request.user.is_authenticated():
		ret['state_code'] = 1
	elif not aPP_id:
		ret['state_code'] = 71
	else:
		app = Application.objects.filter(id=app_id)
		if len(act) == 0:
			ret['state_code'] = 72
		elif has_permission(request.user, app[0].activity):

		else:
			ret['state_code'] = 3
	return HttpResponse(json.dumps(ret), content_type='application/json')












