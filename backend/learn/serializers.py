from django.contrib.auth.models import User
from rest_framework import serializers
from learn.models import Block, Toolbox, Level, Task, Instruction, Student


class UserSerializer(serializers.HyperlinkedModelSerializer):
    student = serializers.HyperlinkedIdentityField(view_name='student-detail')
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'is_staff', 'student')


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ('url', 'id', 'name', 'order')


class ToolboxSerializer(serializers.ModelSerializer):
    blocks = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)

    class Meta:
        model = Toolbox
        fields = ('url', 'id', 'name', 'blocks')


class LevelSerializer(serializers.ModelSerializer):
    tasks = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    class Meta:
        model = Level
        fields = ('url', 'id', 'name', 'credits', 'toolbox', 'tasks')


class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = ('url', 'id', 'name')


class TaskSerializer(serializers.ModelSerializer):
    level = serializers.SlugRelatedField(slug_field='name', many=False, read_only=True)
    class Meta:
        model = Task
        fields = ('url', 'id', 'name', 'level', 'setting', 'solution')


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    user = serializers.HyperlinkedIdentityField(view_name='user-detail')
    practice_overview = serializers.HyperlinkedIdentityField(
            view_name='student-practice-overview')

    class Meta:
        model = Student
        fields = ('id', 'url', 'username', 'user', 'credits', 'practice_overview')
