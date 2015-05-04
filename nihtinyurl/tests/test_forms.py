# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.test import TestCase

from ..forms import ShortcutURLForm


class TestShortcutURLForm(TestCase):
    form_class = ShortcutURLForm

    def testFormSuccess(self):
        form = self.form_class(data={'target': 'http://mumble.com/blah-blah'})
        self.assertTrue(form.is_valid())

    def testFormFailure(self):
        form = self.form_class(data={'target': 'blah-blah'})
        self.assertFalse(form.is_valid())
