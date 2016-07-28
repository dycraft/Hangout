from .models import Activity, User, Tag
from .serializer import easy_serialize, serialize
from .utilities import cmp_to_key
from django.http import HttpResponse
from django.db.models import Q


import json
from itertools import chain

def weight(obj, keyword):
	weight = 0
	if isinstance(obj, User):
		weight += obj.name.lower().count(keyword.lower()) * 3
		weight += obj.intro.lower().count(keyword.lower())
	elif isinstance(obj, Activity):
		weight += obj.name.lower().count(keyword.lower()) * 3
		weight += obj.intro.lower().count(keyword.lower())
	elif isinstance(obj, Tag):
		weight += len(obj.users.all())
		weight += len(obj.acts.all())
	return weight
		

def compare_construct(keyword):
	def cmp(a, b):
		x = weight(a, keyword) 
		y = weight(b, keyword)
		if x < y:
			return -1
		elif x > y:
			return 1
		else:
			return 0
	return cmp

'''
query:
	search database using the keyword provided

GET param
---------------------------------------------------------------------
| param     | introduction                   | default              |
|===================================================================|
| keyword   | keyword of query               | REQUIRED             |
|===================================================================|

returns:
    'user'
    'act'
    'tag'

'''
def query(request, keyword):

	user = User.objects.filter(Q(name__icontains=keyword) | Q(intro__icontains=keyword))
	act = Activity.objects.filter(Q(name__icontains=keyword) | Q(intro__icontains=keyword))
	tag = Tag.objects.filter(name__icontains=keyword)

	result_user = sorted(user, key=cmp_to_key(compare_construct(keyword)))
	result_act = sorted(act, key=cmp_to_key(compare_construct(keyword)))
	result_tag = sorted(tag, key=cmp_to_key(compare_construct(keyword)))

	ret = dict()
	ret['user'] = []
	ret['act'] = []
	ret['tag'] = []

	for obj in result_user:
		ret['user'].append(easy_serialize(obj))
	for obj in result_act:
		ret['act'].append(serialize(obj))
	for obj in result_tag:
		ret['tag'].append(easy_serialize(obj))

	return HttpResponse(json.dumps(ret), content_type='application/json')
