# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'nihtinyurl/index.html'
