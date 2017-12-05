from django.contrib.auth import login
from django.contrib.auth.models import User
from lazysignup.utils import is_lazy_user
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from learn.credits import get_active_credits, get_level_value
from learn.models import Block, Toolbox, Level, Task, Instruction
from learn.models import Action, ProgramSnapshot, Student, TaskSession
from learn.models import Feedback, Teacher, Classroom
from learn.users import convert_lazy_user
from learn.world import get_world


class UserSerializer(serializers.HyperlinkedModelSerializer):
    nickname = serializers.CharField(read_only=True, source='first_name')
    is_lazy = serializers.SerializerMethodField()
    student = serializers.HyperlinkedRelatedField(
        view_name='student-detail',
        read_only=True)
    teacher = serializers.HyperlinkedRelatedField(
        view_name='teacher-detail',
        read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'url', 'username', 'email', 'nickname', 'is_staff', 'is_lazy',
            'student', 'teacher')

    def get_is_lazy(self, user):
        return is_lazy_user(user)


class LazyRegisterSerializer(RegisterSerializer):
    """Extends RegisterSerializer to convert lazy users to registered users.
    """
    def custom_signup(self, request, user):
        if is_lazy_user(request.user):
            lazy_user = request.user
            convert_lazy_user(lazy_user, user)


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
    tasks = serializers.SlugRelatedField(
        slug_field='name',
        many=True,
        read_only=True)
    toolbox = serializers.SlugRelatedField(
        slug_field='name',
        many=False,
        queryset=Toolbox.objects.all())

    class Meta:
        model = Level
        fields = ('url', 'id', 'level', 'name', 'credits', 'toolbox', 'tasks')


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


class WorldSerializer(serializers.Serializer):
    blocks = BlockSerializer(many=True)
    toolboxes = ToolboxSerializer(many=True)
    instructions = InstructionSerializer(many=True)
    levels = LevelSerializer(many=True)
    tasks = TaskSerializer(many=True)


class TeacherSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True,
        required=False)
    classrooms = serializers.SlugRelatedField(
        slug_field='name',
        many=True,
        queryset=Classroom.objects.all())

    class Meta:
        model = Teacher
        fields = ('id', 'url', 'user', 'classrooms')


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True,
        required=False)
    credits = serializers.IntegerField(read_only=True)
    level = serializers.SerializerMethodField()
    seen_instructions = serializers.SlugRelatedField(
        slug_field='name',
        many=True,
        queryset=Instruction.objects.all())
    classroom = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Classroom.objects.all())
    active_credits = serializers.SerializerMethodField()
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
            'id', 'url', 'user', 'credits', 'level', 'active_credits',
            'seen_instructions', 'classroom', 'practice_overview',
            'start_task', 'watch_instruction', 'edit_program', 'run_program')

    def get_active_credits(self, student):
        world = get_world()
        return get_active_credits(world, student)

    def get_level(self, student):
        world = get_world()
        return get_level_value(world, student)


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


class ProgressSerializer(serializers.Serializer):
    level = serializers.IntegerField()
    credits = serializers.IntegerField()
    active_credits = serializers.IntegerField()


class RunProgramResponseSerializer(serializers.Serializer):
    correct = serializers.BooleanField()
    progress = ProgressSerializer(required=False)
    recommendation = RecommendationSerializer(required=False)


class FeedbackSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.pk')
    class Meta:
        model = Feedback
        fields = ('id', 'user', 'email', 'comment', 'url')
