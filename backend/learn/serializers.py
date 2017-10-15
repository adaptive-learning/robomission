from django.contrib.auth.models import User
from rest_framework import serializers
from learn.models import Block, Toolbox, Level, Task, Instruction
from learn.models import Action, ProgramSnapshot, Student, TaskSession


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
    level = serializers.SlugRelatedField(
        slug_field='name',
        many=False,
        queryset=Level.objects.all())

    class Meta:
        model = Task
        fields = ('url', 'id', 'name', 'level', 'setting', 'solution')


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    user = serializers.HyperlinkedIdentityField(view_name='user-detail')
    credits = serializers.IntegerField(read_only=True)
    practice_overview = serializers.HyperlinkedIdentityField(
        view_name='student-practice-overview')
    start_task = serializers.HyperlinkedIdentityField(
        view_name='student-start-task')
    watch_instruction = serializers.HyperlinkedIdentityField(
        view_name='student-watch-instruction')
    edit_program = serializers.HyperlinkedIdentityField(
        view_name='student-edit-program')
    run_program = serializers.HyperlinkedIdentityField(
        view_name='student-run-program')

    class Meta:
        model = Student
        fields = (
            'id', 'url', 'username', 'user', 'credits',
            'practice_overview',
            'start_task', 'watch_instruction', 'edit_program', 'run_program')


class TaskSessionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TaskSession
        fields = ('url', 'id', 'student', 'task', 'solved', 'start', 'end')
        read_only_fields = ('student', 'solved', 'start', 'end')
        # Student field is made read-only as it should be determined by the
        # current user and passed by TaskSessionsViewSet.perform_create().


class ProgramSnapshotSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProgramSnapshot
        fields = ('url', 'id', 'task_session', 'time', 'program', 'granularity', 'correct')


class ActionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Action
        fields = ('url', 'id', 'name', 'student', 'task', 'time', 'randomness', 'data')


class StudentInstructionSerializer(serializers.Serializer):
    name = serializers.CharField()
    seen = serializers.BooleanField()


class StudentTaskSerializer(serializers.Serializer):
    name = serializers.CharField()
    attempted = serializers.BooleanField()
    solved = serializers.BooleanField()
    time = serializers.IntegerField()  # number of seconds


class RecommendationSerializer(serializers.Serializer):
    available = serializers.BooleanField()
    task = serializers.CharField()


class PracticeOverviewSerializer(serializers.Serializer):
    level = serializers.IntegerField()
    credits = serializers.IntegerField()
    active_credits = serializers.IntegerField()
    instructions = StudentInstructionSerializer(many=True)
    tasks = StudentTaskSerializer(many=True)
    recommendation = RecommendationSerializer()
