from django.contrib.auth.models import User
from rest_framework import serializers
from learn.models import Block, Toolbox, Student


class UserSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'student')


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
    id = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Student
        fields = ('id', 'username', 'credits')
