# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-10 22:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ip_manager', '0003_auto_20161010_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subnet',
            name='last_sweep',
            field=models.DateTimeField(null=True),
        ),
    ]
