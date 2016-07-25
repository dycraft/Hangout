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
    url(r'^user/detail/(?P<email>.*?)$', user.get_user),
    url(r'^user/update$', user.update_user),
    url(r'^user/delete$', user.delete_user),
    url(r'^user/update_password$', user.update_password),

    # User messages
    url(r'^user/message/get$', user.get_message),
    url(r'^user/message/send$', user.send_message_post),

    # User and Activity
    url(r'^user/apply$', user.apply_for_activity),
    url(r'^user/quit_act$', user.quit_activity),

    # Activity
    url(r'^activity/create$', activity.create_activity),
    url(r'^activity/detail$', activity.get_activity_detail),

    # Activity admin
    url(r'^activity/update$', activity.update_activity),
    url(r'^activity/applications$', activity.get_applications),


### for testing 
    url(r'^test$', user.testauthentication)

]
