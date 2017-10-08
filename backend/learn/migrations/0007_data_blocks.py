"""Data migration creating blocks.
"""
from django.db import migrations


def create_blocks(apps, schema_editor):
    Block = apps.get_model('learn', 'Block')
    blocks = [
        Block(id=1, name='fly', order=1),
        Block(id=2, name='shoot', order=2),
        Block(id=3, name='repeat', order=3),
        Block(id=4, name='while', order=4),
        Block(id=5, name='color', order=5),
        Block(id=6, name='position', order=6),
        Block(id=7, name='if', order=7),
        Block(id=8, name='if-else', order=8),
    ]
    for block in blocks:
        block.save()


def remove_blocks(apps, schema_editor):
    Block = apps.get_model('learn', 'Block')
    db_alias = schema_editor.connection.alias
    Block.objects.using(db_alias).all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0006_data_instructions'),
    ]

    operations = [
        migrations.RunPython(create_blocks, reverse_code=remove_blocks),
    ]
