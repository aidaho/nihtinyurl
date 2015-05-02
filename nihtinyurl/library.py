# -*- coding: utf-8 -*-
"""
Collection of shared convenience functions.
"""
from __future__ import absolute_import, unicode_literals

import importlib
import re

from django.conf import settings


def get_site_root_paths():
    """
    Returns dictionary of first-level path members in use.

    Example: {'admin': '^admin/doc/'}

    :rtype: dict
    """
    root_urlconf_pattern = re.compile('^\^(?P<word>[\w-]+)/.*')
    url_patterns = {}
    # Get site root urlconf:
    urls = importlib.import_module(settings.ROOT_URLCONF)

    # Walk through root urlconf and collect all collision-prone urls:
    for p in urls.urlpatterns:
        match = root_urlconf_pattern.match(p.regex.pattern)
        if match:
            url_patterns[match.group('word')] = p.regex.pattern

    return url_patterns
