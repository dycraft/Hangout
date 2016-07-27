

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