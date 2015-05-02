# -*- coding: utf-8 -*-
"""
This command adds words from supplied word list to the DB.

Repeated invocation with duplicates is safe. Words are being slugified.
"""
from __future__ import absolute_import, unicode_literals

import os
import re

from django.core.management.base import BaseCommand, CommandError
from django.db.transaction import atomic

from ... import urls
from ...library import get_site_root_paths
from ...models import Shortcut


class Command(BaseCommand):
    help = "Imports words from the supplied file into DB."

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('wordlist', nargs='+', type=str,
                            help="plain text file with words separated by newlines")

    @atomic
    def handle(self, *args, **options):
        shortcut_pattern = Shortcut.get_keyword_filter_pattern()
        url_patterns = get_site_root_paths()  # holds existing URL patterns to avoid
        stats = {'ignored': 0, 'imported': 0, 'duplicates': 0}

        # Iterate through supplied file paths
        for fpath in options['wordlist']:
            wordlist = open(os.path.abspath(fpath), 'r')

            for line in wordlist:
                # Convert line to lowercase and remove unwanted chars:
                word = shortcut_pattern.sub('', line.lower())
                if not word:
                    continue  # skip empty lines

                if word in url_patterns:  # collision check
                    self.stderr.write(
                        "[WW] Ignored line '{0}' from <{2}>. Reason: clash with "
                        "'{1}' url pattern.".format(line.rstrip('\n'), url_patterns[word],
                                                    os.path.basename(fpath))
                    )
                    stats['ignored'] += 1
                    continue

                shortcut, created = Shortcut.objects.get_or_create(keyword=word)
                if created:
                    stats['imported'] += 1
                else:
                    stats['duplicates'] += 1

            wordlist.close()

        self.stdout.write(
            "\nImport complete. {imported} shortcuts imported, {ignored} "
            "ignored, {duplicates} already in DB".format(**stats)
        )
