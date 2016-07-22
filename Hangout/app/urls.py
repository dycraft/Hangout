from django.conf.urls import url
from . import user, activity

app_name = 'app'

urlpatterns = [
    #login/logout
    url(r'^login', user.user_login),
    url(r'^logout', user.user_logout),
    url(r'^register', user.user_register),
    
    # User
    url(r'^user/login_detail$', user.login_detail),
    url(r'^user/detail$', user.get_user),
    url(r'^user/update$', user.update_user),
    url(r'^user/delete$', user.delete_user),
    url(r'^user/update_password$', user.update_password),

    
    # Activity
    url(r'^activity/create$', activity.create_activity),
    url(r'^activity/detail$', activity.get_activity_detail),
]