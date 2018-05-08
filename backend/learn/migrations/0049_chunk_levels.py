# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-08 08:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0048_problemset_base_manager'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chunk',
            options={'ordering': ['type', 'level', 'level2', 'level3']},
        ),
        migrations.RemoveField(
            model_name='chunk',
            name='section',
        ),
        migrations.AddField(
            model_name='chunk',
            name='level',
            field=models.PositiveSmallIntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='chunk',
            name='level2',
            field=models.PositiveSmallIntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='chunk',
            name='level3',
            field=models.PositiveSmallIntegerField(blank=True, default=None, null=True),
        ),
    ]
