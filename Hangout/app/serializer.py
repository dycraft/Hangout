from .models import User

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

	for f in normal_fields:
		ret[f] = getattr(user, f)

	for f in activity_fields:
		ret[f] = []
		for i in getattr(user, f).all():
			ret[f].append(activity_serialize(i))

	return ret

def activity_serialize(act):

	ret = dict()

	normal_fields = [
		'id',
		'name',
		'intro',
		'cost',		
		'organizer_id'
	]
	manytomany_fields = [
		'tags'
	]

	for f in normal_fields:
		ret[f] = getattr(act, f)

	return ret