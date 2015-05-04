# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import random
import string

from django.test import TestCase
from model_mommy import mommy

from ..models import Shortcut


def make_valid_keyword():
    """
    Returns valid random :class:`~.Shortcut` keyword.

    :rtype: basestring
    """
    pattern = Shortcut.get_keyword_filter_pattern()
    candidate = ''.join(random.sample(string.ascii_lowercase + string.digits, 20))
    return pattern.sub('', candidate)


class ShortcutTestCase(TestCase):
    """Provides couple of random shortcuts for every test along with handy attributes."""
    url = "http://mumble.com/blah-blah"
    keyword = 'blah'

    def setUp(self):
        self.shortcuts = mommy.prepare(Shortcut, _quantity=10)
        for s in self.shortcuts:
            s.keyword = make_valid_keyword()
            s.save()
        super(ShortcutTestCase, self).setUp()
