# coding=utf-8
from .models import *
from django.http import HttpResponse
from .tag import *
from .serializer import *

import json

def create_activity(request):
	ret = dict()
	if not request.user.is_authenticated():
		ret['error'] = 'user not logged in'
	elif request.method == 'POST':
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
	else:
		ret['error'] = 'need post'

	return HttpResponse(json.dumps(ret), content_type='application/json')

def get_activity_detail(request):
	ret = dict()
	if :
		pass