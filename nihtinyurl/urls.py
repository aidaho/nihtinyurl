# -*- coding: utf-8 -*-
"""
Root URL configuration.
"""
from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from django.contrib import admin

from .views import HomePageView

admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'nihtinyurl.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomePageView.as_view(), name='home'),
]
