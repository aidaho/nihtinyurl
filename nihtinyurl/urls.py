# -*- coding: utf-8 -*-
"""
Root URL configuration.
"""
from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from django.contrib import admin

from .views import HomePageView, ShortcutRedirectView, ShortenedURLView

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^url/(?P<keyword>\w+)/$', ShortenedURLView.as_view(), name='shortcut_detail'),
    url(r'^(?P<keyword>\w+)/$', ShortcutRedirectView.as_view(), name='shortcut_redirect'),
]
