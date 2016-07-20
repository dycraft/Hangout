"""Hangout URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, patterns, include
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'app.view.index'),

    # User
    url(r'^api/user/create$', 'app.user.create_user'),
    url(r'^api/user/(?P<user_id>.*?)/request', 'app.user.get_user'),
    url(r'^api/user/(?P<user_id>.*?)/update', 'app.user.update_user'),
    url(r'^api/user/(?P<user_id>.*?)/delete', 'app.user.delete_user'),
    
)
