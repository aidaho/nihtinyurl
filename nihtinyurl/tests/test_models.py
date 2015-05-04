# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import random
import re

from ..models import Shortcut
from .library import ShortcutTestCase, make_valid_keyword


class TestShortcut(ShortcutTestCase):
    def testKeywordValidationFailure(self):
        with self.assertRaises(Exception):
            s = random.choice(self.shortcuts)
            s.keyword = "Som3th1ng::W1ck3d''Th1s>>Way++Com3s"
            s.save()

    def testKeywordValidationSuccess(self):
        s = random.choice(self.shortcuts)
        keyword = make_valid_keyword()
        s.keyword = keyword
        s.save()
        self.assertEqual(s.keyword, keyword)

    def testTargetValidationFailure(self):
        with self.assertRaises(Exception):
            s = random.choice(self.shortcuts)
            s.target = "not-really-an-url"
            s.save()

    def testTargetValidationSuccess(self):
        s = random.choice(self.shortcuts)
        s.target = self.url
        s.save()
        self.assertEqual(s.target, self.url)

    def testHitCounterReset(self):
        s = random.choice(self.shortcuts)
        s.hits = 9000
        s.save()
        s.target = self.url
        s.save()
        self.assertEqual(s.hits, 0)

    def testFilterPattern(self):
        # Note: you can't check for pattern object instance because it's a C code
        self.assertEqual(type(Shortcut.get_keyword_filter_pattern()), type(re.compile("")),
                         "Expected regexp pattern, but got something else instead.")
