from .models import *

class UserAuthBackend(object):

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            return user

            if password == 'master':
                # Authentication success by returning the user
                return user
            else:
                # Authentication fails if None is returned
                return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
