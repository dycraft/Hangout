

def send_application(user_name, act_name, admin_name, app_type):
	tmp = ''
	if app_type == '1':
		tmp = 'a member'
	elif app_type == '2':
		tmp = 'an admin'
	else:
		tmp = 'something'
	msg = 'Dear ' + admin_name + ''':
	''' + user_name + ' wants to be ' + tmp + ' of activity ' + act_name + '.'
	return msg

def application_granted(user_name, app_type, act_name, admin):
	tmp = ''

	if app_type == 1:
		tmp = 'a member'
	elif app_type == 2:
		tmp = 'an admin'

	msg = 'Dear ' + user_name + ''':
	Your application of being ''' + tmp + ' of activity ' + act_name + ' has been GRANTED by ' + admin + '.'
	return msg


def application_rejected(user_name, app_type, act_name, admin, reason=0):
	'''
	reasons
	0: no reason
	1: apply for admin without being a member
	'''
	tmp = ''

	if app_type == 1:
		tmp = 'a member'
	elif app_type == 2:
		tmp = 'an admin'
	r = ''
	if reason == 1:
		r = ' Reason: you are applying for admin without being a member'

	msg = 'Dear ' + user_name + ''':
	Your application of being ''' + tmp + ' of activity \'' + act_name + '\' has been REJECTED by ' + admin + '.' + r
	return msg

def activity_update(act_name, admin_name, user_name):
	msg = 'Dear ' + user_name + ''':
	Information of activity \'''' + act_name + '\' is updated by ' + admin_name + '. Please check it out now!'
	return msg

def kicked_out(act_name, admin_name, user_name):
	msg = 'Dear ' + user_name + ''':
	Your have been kicked out of activity \'''' + act_name + '\' by ' + admin_name + '.'
	return msg

