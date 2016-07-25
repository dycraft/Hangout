from .models import *

def authentication(request, **kwargs):

    required_param = kwargs.get('required_param', [])
    require_authenticate = kwargs.get('require_authenticate', False)
    require_model = kwargs.get('require_model', False)
    require_permission = kwargs.get('require_permission', False)
    model = kwargs.get('model')
    keytype = kwargs.get('keytype', 'id')
    # key = kwargs.get('key')

    ret = dict()
    params = dict()
### check each required param
    for p in required_param:
        params[p] = request.POST.get(p)
        if not params[p]:
            ret['state_code'] = 101
            return ret

    if keytype in params:
	    key = params[keytype]

### check if user has logged in 
    if require_authenticate:
        if not request.user.is_authenticated():
            ret['state_code'] = 1
            return ret

### check permission
    if require_permission == True:
        if not key:
            ret['state_code'] = 104
            return ret
        elif not (request.user.is_admin == True or getattr(request.user, keytype) == key):
            ret['state_code'] = 3
            return ret

### check model
    if require_model == True and model and key:
        if keytype == 'id':
            record = model.objects.filter(id=key)
        elif keytype == 'email':
            record = model.objects.filter(email=key)
        else:
            ret['state_code'] = 102
            return ret

        if len(record) == 0:
            ret['state_code'] = 103
            return ret
        else:
            ret['record'] = record[0]
            ret['state_code'] = 0

    ret['state_code'] = 0
    ret['params'] = params
    return ret

def send_message(from_user, to_user, content):
    if from_user.id == to_user.id:
        return False
    else:
        Message.objects.create(
                from_user=from_user,
                to_user=to_user,
                content=content
            )
        return True