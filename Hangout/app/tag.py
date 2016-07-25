from django.http import HttpResponse
from .models import *

import json


def get_tag(name):
	
	try:
		tag = Tag.objects.get(name=name)
	except Tag.DoesNotExist:
		tag = Tag.objects.create(name=name)

	return tag

def get_tag_detail(request, name):
	ret = dict()
	tag = Tag.objects.filter(name=name)
	if len(tag) == 0:
		ret['state_code'] = 21
	else:
		tag = tag[0]
		ret['state_code'] = 0
		ret['users'] = []
		ret['acts'] = []
		for u in tag.users.all():
			ret['users'].append({'id': u.id, 'name': u.name})
		for a in tag.acts.all():
			ret['acts'].append({'id': a.id, 'name': a.name})
	
	return HttpResponse(json.dumps(ret), content_type='application/json')
