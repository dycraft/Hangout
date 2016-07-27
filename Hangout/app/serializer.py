from .models import *

def user_serialize(user, detailed=True):
	
	ret = dict()

	normal_fields = [
		'id',
		'name', 
		'cellphone',
        'intro',
		'score', 
		'email',
		'fix_times',
		'tmp_times',
		'state',
	]

	activity_fields = []
	if detailed == True:
		activity_fields = [
			'join_acts',
			'admin_acts',
			# 'coll_acts',
		]

### normal fields
	for f in normal_fields:
		ret[f] = getattr(user, f)

## activity fields
	for f in activity_fields:
		ret[f] = []
		for i in getattr(user, f).all():
			ret[f].append({'name': i.name, 'id': i.id, 'state': i.state % 4, 'count': len(i.members.all()) + len(i.admins.all()), 'organizer': {
				'name': i.organizer.name,
				'id': i.organizer.id,
				}})

	# ret['apply_acts'] = []
	# for app in user.applications.filter(application_type=1):
	# 	ret['apply_acts'].append(activity_serialize(app.activity))

### tags
	ret['tags'] = []
	for t in user.tags.all():
		ret['tags'].append(t.name)
	ret['tags'] = ",".join(ret['tags'])
	return ret

def activity_serialize(act, detailed=True):

	ret = dict()

	normal_fields = [
		'id',
		'name',
		'intro',
		'cost',
		'location',
	]
### normal fields
	for f in normal_fields:
		ret[f] = getattr(act, f)
### state
	ret['state'] = act.state % 4
	ret['member_limit'] = act.state >> 2
	ret['member_count'] = len(act.members.all())

### tags
	ret['tags'] = []
	for t in act.tags.all():
		ret['tags'].append(t.name)

	ret['organizer'] = {'id': act.organizer.id, 'name': act.organizer.name}

## times
	ret['time'] = act.time.strftime('%Y-%m-%d %a %H:00')
	ret['create_at'] = act.create_at.strftime('%Y-%m-%d, %H:%M:%S')
	ret['modified_at'] = act.modified_at.strftime('%Y-%m-%d, %H:%M:%S')

	if detailed == True:
		member_fields = [
			'members',
			'admins',
		]

		for field in member_fields:
			ret[field] = []
			for m in getattr(act, field).all():
				ret[field].append({'id': m.id, 'name': m.name})

	return ret

def application_serialize(app):
	ret = dict()

	ret['id'] = app.id
	ret['applicant'] = app.applicant.email
	ret['application_type'] = app.get_application_type_display()
	ret['activity'] = {
		'id': app.activity.id,
		'name': app.activity.name,
	}
	ret['intro'] = app.intro
	ret['time'] = app.time.strftime('%Y-%m-%d %H:%M')
	return ret

def message_serialize(msg):
	ret = dict()
	ret['id'] = msg.id
	ret['from'] = msg.from_user.email
	ret['to'] = msg.to_user.email
	ret['content'] = msg.content
	ret['time'] = msg.time.strftime('%Y-%m-%d %H:%M:%S')
	ret['read'] = msg.read
	return ret

def serialize(obj):
	if isinstance(obj, User):
		return user_serialize(obj)
	elif isinstance(obj, Activity):
		return activity_serialize(obj)
	elif isinstance(obj, Application):
		return application_serialize(obj)
	elif isinstance(obj, Message):
		return message_serialize(obj)
	else:
		return {'error': 'unsupported type'}

def easy_serialize(obj):
	if isinstance(obj, User):
		return {'id': obj.id, 'name': obj.name}
	elif isinstance(obj, Activity):
		return activity_serialize(obj)
	elif isinstance(obj, Application):
		return application_serialize(obj)
	elif isinstance(obj, Message):
		return message_serialize(obj)
	else:
		return {'error': 'unsupported type'}

