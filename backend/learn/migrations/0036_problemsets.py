# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-09 15:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0035_domainparam'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProblemSet',
            fields=[
                ('section', models.CharField(max_length=20)),
                ('level', models.SmallIntegerField()),
                ('setting', jsonfield.fields.JSONField()),
                ('granularity', models.CharField(choices=[('mission', 'mission'), ('phase', 'phase')], default='phase', help_text='Hierachy level; either base phase, or compound mission.', max_length=10)),
                ('chunk', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='problemset_obj', serialize=False, to='learn.Chunk')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='parts', to='learn.ProblemSet')),
            ],
            bases=('learn.chunk',),
        ),
        migrations.RemoveField(
            model_name='mission',
            name='chunk',
        ),
        migrations.RemoveField(
            model_name='chunk',
            name='setting',
        ),
        migrations.RemoveField(
            model_name='chunk',
            name='subchunks',
        ),
        migrations.RemoveField(
            model_name='chunk',
            name='tasks',
        ),
        migrations.RemoveField(
            model_name='domain',
            name='chunks',
        ),
        migrations.RemoveField(
            model_name='domain',
            name='missions',
        ),
        migrations.RemoveField(
            model_name='domainparam',
            name='task',
        ),
        migrations.AddField(
            model_name='task',
            name='order',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='name',
            field=models.SlugField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.SlugField(blank=True, default=''),
        ),
        migrations.DeleteModel(
            name='Mission',
        ),
        migrations.AddField(
            model_name='domain',
            name='problemsets',
            field=models.ManyToManyField(to='learn.ProblemSet'),
        ),
        migrations.AddField(
            model_name='task',
            name='problemset',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks', to='learn.ProblemSet'),
        ),
    ]
