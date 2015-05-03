# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms

from .models import Shortcut


class ShortcutURLForm(forms.ModelForm):
    """URL input form."""
    def __init__( self, *args, **kwargs ):
        super(ShortcutURLForm, self).__init__( *args, **kwargs )
        self.fields['target'].label = ''

    class Meta:
        model = Shortcut
        fields = ['target']
