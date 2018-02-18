"""jsonstorage URL Configuration

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
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin

from core import views as coreviews

import django_eventstream

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    
    url(r'^storage/(?P<application>\w+)/(?P<collection>\w+)$', coreviews.post_data),
    url(r'^storage/(?P<application>\w+)/(?P<collection>\w+)/(?P<ident>\w+)$', coreviews.get_data),
    url(r'^list/(?P<application>\w+)/(?P<collection>\w+)', coreviews.get_data_list),
    url(r'^delete/(?P<application>\w+)/(?P<collection>\w+)', coreviews.delete_data_list),
    url(r'^setup/(?P<application>\w+)/(?P<collection>\w+)', coreviews.get_data_list),
    
    # client selects the channels using query parameters:
    url(r'^events/', include(django_eventstream.urls)),
    
    # client selects a single channel using a path component
    url(r'^events/(?P<channel>\w+)/', include(django_eventstream.urls)),
]
