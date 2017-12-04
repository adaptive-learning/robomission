from django.contrib.auth import login
from django.contrib.auth.models import User
from lazysignup.models import LazyUser
from lazysignup.utils import is_lazy_user
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from learn.credits import get_active_credits, get_level_value
from learn.models import Block, Toolbox, Level, Task, Instruction
from learn.models import Action, ProgramSnapshot, Student, TaskSession
from learn.models import Feedback, Teacher, Classroom
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
        assert is_lazy_user(request.user)
        lazy_user = request.user
        if hasattr(lazy_user, 'student'):
            # TODO: Don't create students automatically with new users, then
            # remove the following line, which prevents error (unique
            # constraint vialation) due to 2 students for 1 user.
            user.student.delete()
            lazy_user.student.user = user
            lazy_user.student.save()
        # TODO: rewire teacher as well
        delete_lazy_user(lazy_user)

    #def save(self, request):
    #    user = request.user
    #    data = self.get_cleaned_data()
    #    username = data['username']
    #    email = data['email']
    #    password = data['password1']
    #    assert email == username
    #    user = convert_lazy_user(user, email, password)
    #    # Automatically login the user after succesful registration.
    #    login(request, user)
    #    return user


#def convert_lazy_user(user, email, password):
#    """Convert a lazy user into a registered user.
#
#    Sets email and password.
#    Deletes the LazyUser record to mark the user as non-lazy.
#    """
#    assert is_lazy_user(user)
#    # We use email as the unique username.
#    user.username = email
#    user.email = email
#    user.set_password(password)
#    delete_lazy_user(user)
#    # Set default authentication backend.
#    user.backend = None
#    user.save()
#    assert not is_lazy_user(user)
#    return user


def delete_lazy_user(user):
    LazyUser.objects.filter(user=user).delete()


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
