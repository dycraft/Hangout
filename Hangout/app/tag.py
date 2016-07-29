from django.http import HttpResponse
from .models import *
from .serializer import easy_serialize

import json


def get_tag(name):
	
	# try:
	# 	tag = Tag.objects.get(name=name)
	# except Tag.DoesNotExist:
	# 	tag = Tag.objects.create(name=name)

	return Tag.objects.get_or_create(name=name)[0]

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
			ret['users'].append(easy_serialize(u))
		for a in tag.acts.all():
			ret['acts'].append(easy_serialize(a))
	
	return HttpResponse(json.dumps(ret), content_type='application/json')
