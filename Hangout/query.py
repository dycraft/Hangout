from .models import Activity, User, Tag
from itertools import chain


def weight(obj):
	weight = 0
	if isinstance(obj, User):
		

def compare(a, b):
	pass


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
    'state_code'
    'user_info' -- when (state_code == 0)

'''
def query(request, keyword):

	user_name = User.objects.filter(name__icontains=keyword)
	user_intro = User.objects.filter(into__icontains=keyword)

	act_name = Activity.objects.filter(name__icontains=keyword)
	act_intro = Activity.objects.filter(into__icontains=keyword)

	tag = Tag.objects.filter(name__icontains=keyword)

	union = chain(user_name, user_intro, act_name, act_intro, tag)

	# sort()