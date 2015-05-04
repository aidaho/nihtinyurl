# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import time

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from ..models import Shortcut
from .library import ShortcutTestCase


class HomePageTest(ShortcutTestCase):
    def testGET(self):
        c = Client()
        r = c.get(reverse('home'))
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.context['form'], "URL form is missing!")

    def testPOST(self):
        Shortcut.objects.create(keyword=self.keyword)
        c = Client()
        r = c.post(reverse('home'), {'target': self.url})
        # We also simultaneously check keyword to url corellation
        self.assertRedirects(r, reverse('shortcut_detail', kwargs={'keyword': self.keyword}))

    def testShortcutReuse(self):
        new_url = 'http://te.st/reuse'
        for s in self.shortcuts:
            s.target = self.url
            s.save()
            time.sleep(0.01)  # give instances a little space in time

        oldest = Shortcut.objects.earliest('updated')
        # All shortcuts are claimed at this point
        c = Client()
        c.post(reverse('home'), {'target': new_url})
        updated = Shortcut.objects.get(target=new_url)
        self.assertEqual(oldest.pk, updated.pk,
                         "When no available shorcuts left, the oldest one should be reused.")


class ShortcutDetailTest(TestCase):
    url = "http://mumble.com/blah-blah"
    keyword = 'test'

    def testGET(self):
        Shortcut.objects.create(keyword=self.keyword, target=self.url)
        c = Client()
        r = c.get(reverse('shortcut_detail', kwargs={'keyword': self.keyword}))
        self.assertEqual(r.status_code, 200)
