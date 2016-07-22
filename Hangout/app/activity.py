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
		ret['error'] = 'user not logged in'
	else:
		ret['name'] = request.POST.get('name', 'untitled')
		ret['intro'] = request.POST.get('intro', 'No intro available')
		ret['tags'] = request.POST.get('tag', '').split('&&')
		ret['cost'] = request.POST.get('cost', 0)
		ret['organizer_id'] = request.user.id
		act = Activity.objects.create(
				name=ret['name'],
				intro=ret['intro'],
				cost=ret['cost'],
				organizer_id=request.user.id,
			)
		for t in ret['tags']:
			act.tags.add(get_tag(t))
		act.save()

	return HttpResponse(json.dumps(ret), content_type='application/json')

@require_http_methods(['POST'])
def get_activity_detail(request):
	ret = dict()
	act_id = request.POST.get('act_id')
	if not act_id:
		ret['error'] = 'need act_id'
	else:
		try:
			act = Activity.objects.get(id=act_id)
			ret = activity_serialize(act)
		except Activity.DoesNotExist:
			ret['error'] = 'act not exist'
	return HttpResponse(json.dumps(ret), content_type='application/json')

# @require_http_methods(['POST'])
# def update_activity(request):
# 	ret = dict()
# 	act_id = request.POST.get('act_id')
# 	if not act_id:
# 		ret['error'] = 'need act_id'
# 	else:
# 		