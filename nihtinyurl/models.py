# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re

from django.core.exceptions import ValidationError
from django.db import models

from .library import get_site_root_paths


class ModelValidationMixin(object):
    """Calls model's .clean() method prior .save(), if one exists."""
    def save(self, *args, **kwargs):
        if hasattr(getattr(self, 'clean', None), '__call__'):
            self.clean()
        super(ModelValidationMixin, self).save(*args, **kwargs)


class TimeStampedModel(models.Model):
    """Provides creation/modification time tracking for derived models."""
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Shortcut(ModelValidationMixin, TimeStampedModel):
    """A key, which can be used to represent stored long URL."""
    keyword = models.CharField(max_length=64, unique=True)
    target = models.URLField(null=True)
    hits = models.IntegerField(default=0)

    def __unicode__(self):
        return "{0} ({1}): {2}".format(self.keyword, self.hits, self.target)

    @classmethod
    def get_keyword_filter_pattern(cls):
        """
        Returns regex pattern, which matches chars **NOT ALLOWED** in
        :attr:`~Shortcut.keyword`.

        :rtype: RegexURLPattern
        """
        # We would like to evaluate this lazily and only once:
        if not getattr(cls, '_keyword_filter_pattern', None):
            # Match everything out of [a-z0-9] range:
            cls._keyword_filter_pattern = re.compile('[^a-z0-9]+')
        return cls._keyword_filter_pattern

    def clean(self):
        self.clean_keyword()

    def clean_keyword(self):
        if not self.pk:  # check new keyword for clash with site urlpatterns
            url_patterns = get_site_root_paths()
            if self.keyword in url_patterns:
                raise ValidationError(
                    "You cannot create shortcut with keyword '{0}' because "
                    "it clashes with site url pattern '{1}'!".format(
                        self.keyword, url_patterns[self.keyword])
                )
