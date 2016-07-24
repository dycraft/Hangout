# coding=utf-8
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .tag import *
from .serializer import *
from .models import *

import json

### create an activity, user that is currently logged in will be the organizer
@require_http_methods(['POST'])
def create_activity(request):
	ret = dict()
	if not request.user.is_authenticated():
		ret['state_code'] = 1
	else:
		act_info = dict()
		act_info['name'] = request.POST.get('name', 'untitled')
		act_info['intro'] = request.POST.get('intro', 'No intro available')
		act_info['tags'] = request.POST.get('tag', '').split('&&')
		act_info['cost'] = request.POST.get('cost', 0)
		act_info['organizer'] = request.user.email
		act = Activity.objects.create(
				name=act_info['name'],
				intro=act_info['intro'],
				cost=act_info['cost'],
				organizer_id=request.user.id,
			)
		for t in act_info['tags']:
			act.tags.add(get_tag(t))
		act.save()
		ret['state_code'] = 0

	return HttpResponse(json.dumps(ret), content_type='application/json')

@require_http_methods(['POST'])
def get_activity_detail(request):
	ret = dict()
	act_id = request.POST.get('act_id')
	if not act_id:
		ret['state_code'] = 51
	else:
		try:
			act = Activity.objects.get(id=act_id)
			ret['act_info'] = activity_serialize(act)
			ret['state_code'] = 0
		except Activity.DoesNotExist:
			ret['state_code'] = 52
	return HttpResponse(json.dumps(ret), content_type='application/json')

# @require_http_methods(['POST'])
# def update_activity(request):
# 	ret = dict()
# 	act_id = request.POST.get('act_id')
# 	if not act_id:
# 		ret['state_code'] = 51
# 	else:
		