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
		'tmp_times'
	]

	activity_fields = []
	if detailed == True:
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

def activity_serialize(act, detailed=False):

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
	ret['state'] = act.get_state_display()
### tags
	ret['tags'] = []
	for t in act.tags.all():
		ret['tags'].append(t.name)

	ret['organizer'] = act.organizer.email

## times
	ret['time'] = act.time.strftime('%Y-%m-%d %a %H:00')
	ret['create_at'] = act.create_at.strftime('%Y-%m-%d, %H:%M:%S')
	ret['modified_at'] = act.modified_at.strftime('%Y-%m-%d, %H:%M:%S')

	if detailed == True:
		member_fields = [
			'applicants',
			'members',
			'admins',
			'collected',
		]

		for field in member_fields:
			ret[field] = []
			for m in getattr(act, field).all():
				ret[field].append(m.email)

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
