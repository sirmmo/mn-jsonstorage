# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-01-28 11:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_application_site'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='application',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='collections', to='core.Application'),
            preserve_default=False,
        ),
    ]