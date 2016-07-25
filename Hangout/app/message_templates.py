

def application_granted(user_name, app_type, act_name, admin):
	tmp = ''

	if app_type == 1:
		tmp = 'a member'
	elif app_type == 2:
		tmp = 'an admin'

	msg = 'Dear ' + user_name + ''':
	Your application of being ''' + tmp + ' of activity ' + act_name + ' has been GRANTED by ' + admin + '.'
	return msg


def application_refused(user_name, app_type, act_name, admin):
	tmp = ''

	if app_type == 1:
		tmp = 'a member'
	elif app_type == 2:
		tmp = 'an admin'

	msg = 'Dear ' + user_name + ''':
	Your application of being ''' + tmp + ' of activity \'' + act_name + '\' has been REFUSED by ' + admin + '.'
	return msg