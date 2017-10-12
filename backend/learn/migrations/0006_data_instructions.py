"""Data migration creating instructions.
"""
from django.db import migrations


def create_instructions(apps, schema_editor):
    Instruction = apps.get_model('learn', 'Instruction')
    Instruction.objects.all().delete()
    instructions = [
        Instruction(id=1, name='env.space-world'),
        Instruction(id=2, name='env.toolbox'),
        Instruction(id=3, name='env.snapping'),
        Instruction(id=4, name='env.controls'),
        Instruction(id=5, name='env.task-editor'),
        Instruction(id=6, name='object.asteroid'),
        Instruction(id=7, name='object.meteoroid'),
        Instruction(id=8, name='object.diamond'),
        Instruction(id=9, name='object.wormhole'),
        Instruction(id=10, name='diamonds-status'),
        Instruction(id=11, name='energy-status'),
        Instruction(id=12, name='length-limit'),
        Instruction(id=13, name='block.fly'),
        Instruction(id=14, name='block.shoot'),
        Instruction(id=15, name='block.repeat'),
        Instruction(id=16, name='block.while'),
        Instruction(id=17, name='block.color'),
        Instruction(id=18, name='block.position'),
        Instruction(id=19, name='block.if'),
        Instruction(id=20, name='block.if-else')]
    for instruction in instructions:
        instruction.save()


def remove_instructions(apps, schema_editor):
    Instruction = apps.get_model('learn', 'Instruction')
    db_alias = schema_editor.connection.alias
    Instruction.objects.using(db_alias).all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0005_task'),
    ]

    operations = [
        migrations.RunPython(create_instructions, reverse_code=remove_instructions),
    ]
