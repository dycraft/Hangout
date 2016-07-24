from .models import User, Activity

def user_serialize(user):
	
	ret = dict()

	normal_fields = [
		'id',
		'name', 
		'cellphone', 
		'score', 
		'email',
		'fix_times',
		'tmp_times'
	]

	activity_fields = [
		'apply_acts',
		'join_acts',
		'admin_acts',
		'coll_acts',
	]
### normal fields
	for f in normal_fields:
		ret[f] = getattr(user, f)
### activity fields
	for f in activity_fields:
		ret[f] = []
		for i in getattr(user, f).all():
			ret[f].append(activity_serialize(i))
### tags
	ret['tags'] = []
	for t in user.tags.all():
		ret['tags'].append(t.name)
	ret['tags'] = ",".join(ret['tags'])
	return ret

def activity_serialize(act):

	ret = dict()

	normal_fields = [
		'id',
		'name',
		'intro',
		'cost',
		'state',
		'location',
	]
### normal fields
	for f in normal_fields:
		ret[f] = getattr(act, f)
### tags
	ret['tags'] = []
	for t in act.tags.all():
		ret['tags'].append(t.name)

	ret['organizer'] = act.organizer.email

## times
	ret['time'] = act.time.strftime('%Y-%m-%d %a %H:00')
	ret['create_at'] = act.create_at.strftime('%Y-%m-%d, %H:%M:%S')
	ret['modified_at'] = act.modified_at.strftime('%Y-%m-%d, %H:%M:%S')

	return ret
