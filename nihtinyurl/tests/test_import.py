# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os

from django.core import management
from django.test import TestCase

from ..models import Shortcut


class ImportTest(TestCase):
    expect = ["python", "10thavenue", "mcdonalds", "l33t", "z", "hurrdurr", "ome"]
    fixture_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../fixtures/words-tiny.txt'))

    def testImport(self):
        management.call_command('import_shortcuts', self.fixture_path)
        shortcuts = Shortcut.objects.all()
        self.assertEqual(len(shortcuts), len(self.expect))
        for s in shortcuts:
            if s.keyword not in self.expect:
                raise Exception("Imported uninvited shortcut: %s" % s)
