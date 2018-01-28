# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-01-28 11:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('core', '0002_auto_20180126_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='site',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sites.Site'),
            preserve_default=False,
        ),
    ]
