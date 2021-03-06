# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-12 06:28
from __future__ import unicode_literals

from django.db import migrations

def remove_instructions(apps, schema_editor):
    # Simply remove all existing instructions and load them again after
    # the Instruction model is rewired to inherit from Chunks.
    Instruction = apps.get_model('learn', 'Instruction')
    Instruction.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0051_instruction_chunk_ptr'),
    ]

    operations = [
        migrations.RunPython(remove_instructions),
    ]
