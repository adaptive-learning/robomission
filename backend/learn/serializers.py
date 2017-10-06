from rest_framework import serializers
from learn.models import Block, Toolbox, Student


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ('id', 'name', 'order')


class ToolboxSerializer(serializers.ModelSerializer):
    blocks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Toolbox
        fields = ('id', 'name', 'blocks')


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ('credits', )
