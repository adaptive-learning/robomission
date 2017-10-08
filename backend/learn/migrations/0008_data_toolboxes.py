"""Data migration creating toolboxes.
"""
from django.db import migrations
from rest_framework import serializers


TOOLBOXES = [
    {'id': 1, 'name': 'fly',
     'blocks': ['fly']},
    {'id': 2, 'name': 'shoot',
     'blocks': ['fly', 'shoot']},
    {'id': 3, 'name': 'repeat',
     'blocks': ['fly', 'shoot', 'repeat']},
    {'id': 4, 'name': 'while',
     'blocks': ['fly', 'shoot', 'while', 'color']},
    {'id': 5, 'name': 'loops',
     'blocks': ['fly', 'shoot', 'repeat', 'while', 'color']},
    {'id': 6, 'name': 'loops+if',
     'blocks': ['fly', 'shoot', 'repeat', 'while', 'color', 'if']},
    {'id': 7, 'name': 'loops+if+position',
     'blocks': ['fly', 'shoot', 'repeat', 'while', 'color', 'position', 'if']},
    {'id': 8, 'name': 'loops+if+else',
     'blocks': ['fly', 'shoot', 'repeat', 'while', 'color', 'position', 'if', 'if-else']},
    {'id': 9, 'name': 'complete',
     'blocks': ['fly', 'shoot', 'repeat', 'while', 'color', 'position', 'if', 'if-else']}
]


def create_toolboxes(apps, schema_editor):
    Block = apps.get_model('learn', 'Block')
    Toolbox = apps.get_model('learn', 'Toolbox')

    class ToolboxSerializer(serializers.ModelSerializer):
        id = serializers.IntegerField(read_only=False)
        blocks = serializers.SlugRelatedField(
            slug_field='name',
            many=True,
            queryset=Block.objects.all())
        class Meta:
            model = Toolbox
            fields = ('id', 'name', 'blocks')

    serializer = ToolboxSerializer(data=TOOLBOXES, many=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()


def remove_toolboxes(apps, schema_editor):
    Toolbox = apps.get_model('learn', 'Toolbox')
    db_alias = schema_editor.connection.alias
    Toolbox.objects.using(db_alias).all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0007_data_blocks'),
    ]

    operations = [
        migrations.RunPython(create_toolboxes, reverse_code=remove_toolboxes),
    ]
