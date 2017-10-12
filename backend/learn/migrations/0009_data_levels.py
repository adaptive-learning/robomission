"""Data migration creating levels.
"""
from django.db import migrations


def create_levels(apps, schema_editor):
    Level = apps.get_model('learn', 'Level')
    Toolbox = apps.get_model('learn', 'Toolbox')
    toolbox = lambda name: Toolbox.objects.get(name=name)
    Level.objects.all().delete()
    levels = [
        Level(id=1, level=1, name='moves', toolbox=toolbox('fly'), credits=6),
        Level(id=2, level=2, name='world', toolbox=toolbox('shoot'), credits=25),
        Level(id=3, level=3, name='repeat', toolbox=toolbox('repeat'), credits=40),
        Level(id=4, level=4, name='while', toolbox=toolbox('while'), credits=60),
        Level(id=5, level=5, name='loops', toolbox=toolbox('loops'), credits=100),
        Level(id=6, level=6, name='if', toolbox=toolbox('loops+if'), credits=150),
        Level(id=7, level=7, name='comparing', toolbox=toolbox('loops+if+position'), credits=200),
        Level(id=8, level=8, name='if-else', toolbox=toolbox('loops+if+else'), credits=300),
        Level(id=9, level=9, name='final-challenge', toolbox=toolbox('complete'), credits=1000),
    ]
    for level in levels:
        level.save()


def remove_levels(apps, schema_editor):
    Level = apps.get_model('learn', 'Level')
    db_alias = schema_editor.connection.alias
    Level.objects.using(db_alias).all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0008_data_toolboxes'),
    ]

    operations = [
        migrations.RunPython(create_levels, reverse_code=remove_levels),
    ]
