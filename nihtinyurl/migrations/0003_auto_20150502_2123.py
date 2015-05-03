# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nihtinyurl', '0002_shortcut_hits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shortcut',
            name='target',
            field=models.URLField(max_length=2047, null=True),
        ),
    ]
