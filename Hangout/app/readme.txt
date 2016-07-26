Error code 

### user

0: success
1: user not logged in 
2: user does not exist
3: permission denied
4: email not provided
5: password not provided
6: user already logged in
7: user is frozen by admin
8: wrong email/password
9: invalid email/password
10: email address already in use
11: unrecognized param value

### tag
21 tag does not exist

### message
31 message does not exist
32 unrecognized message state

### activity
51: act_id not provided
52: act does not exist
53: application already sent
54: user is not a member
55: user is already a member
56: user is already an admin

### application
71: application_id not provided
72: application does not exist

###
101: required key not provided
102: unsupported model keytype
103: record does not exist
104: no key to check permission with


authentication params
	required_param
	require_authenticate
	require_model
	require_permission
	model
	keytype