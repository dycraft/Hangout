from django.conf.urls import url
from . import user, activity, tag, query

app_name = 'app'

urlpatterns = [
    #login/logout
    url(r'^login', user.user_login),
    url(r'^logout', user.user_logout),
    url(r'^register', user.user_register),
    
    # User
    url(r'^user/exist/(?P<email>.*?)$', user.user_exist),
    url(r'^user/login_detail$', user.login_detail),
    url(r'^user/detail/(?P<id>.*?)$', user.get_user),
    url(r'^user/update$', user.update_user),
    url(r'^user/delete$', user.delete_user),
    url(r'^user/update_password$', user.update_password),

    url(r'^user/follow$', user.follow),
    url(r'^user/unfollow$', user.unfollow),
    url(r'^user/following$', user.check_following),
    url(r'^user/follower$', user.check_follower),

    # User messages
    url(r'^user/message/get$', user.get_message),
    url(r'^user/message/send$', user.send_message_post),
    url(r'^user/message/set_state/(?P<id>.*?)/(?P<state>.*?)$', user.set_message_state),

    # User and Activity
    url(r'^user/get_admin_act', user.get_admin_activity),
    url(r'^user/get_join_act', user.get_join_activity),
    url(r'^user/apply$', user.apply_for_activity),
    url(r'^user/quit_act$', user.quit_activity),

    # Activity
    url(r'^activity/create$', activity.create_activity),
    url(r'^activity/detail/(?P<id>.*?)$', activity.get_activity_detail),
    url(r'^activity/change_state', activity.change_act_state),

    # Activity admin
    url(r'^activity/update$', activity.update_activity),
    url(r'^activity/applications$', activity.get_applications),
    url(r'^activity/reply_application$', activity.reply_application),
    url(r'^activity/recommended_time/(?P<id>.*?)$', activity.get_recommended_time),

    # Tag
    url(r'^tag/get/(?P<name>.*?)$', tag.get_tag_detail),

    # Query
    url(r'^search/(?P<keyword>.*?)$', query.query),


### for testing 
    url(r'^test$', user.testauthentication),

]
