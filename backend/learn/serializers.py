from django.contrib.auth.models import User
from rest_framework import serializers
from learn.models import Block, Toolbox, Student


class UserSerializer(serializers.HyperlinkedModelSerializer):
    student = serializers.HyperlinkedIdentityField(view_name='student-detail')
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'is_staff', 'student')


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
    user = serializers.HyperlinkedIdentityField(view_name='user-detail')
    practice_overview = serializers.HyperlinkedIdentityField(
            view_name='student-practice-overview')

    class Meta:
        model = Student
        fields = ('id', 'url', 'username', 'user', 'credits', 'practice_overview')
