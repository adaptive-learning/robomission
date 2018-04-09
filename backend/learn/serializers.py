from django.contrib.auth import login
from django.contrib.auth.models import User
from lazysignup.utils import is_lazy_user
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from learn.domain import get_domain
from learn.mastery import get_level
from learn.models import Block, Toolbox, Task, Instruction
from learn.models import Action, ProgramSnapshot, Student, TaskSession
from learn.models import Teacher, Classroom
from learn.models import Chunk, Mission, Domain
from learn.users import convert_lazy_user, is_initial_user


class UserSerializer(serializers.HyperlinkedModelSerializer):
    nickname = serializers.CharField(read_only=True, source='first_name')
    created = serializers.SerializerMethodField()
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
            'id', 'url', 'username', 'email', 'nickname',
            'is_staff', 'is_lazy', 'created',
            'student', 'teacher')

    def get_is_lazy(self, user):
        # TODO: rename to is_anonymous
        return is_lazy_user(user) or user.is_anonymous() or is_initial_user(user)

    def get_created(self, user):
        return not is_initial_user(user)


class LazyRegisterSerializer(RegisterSerializer):
    """Extends RegisterSerializer to convert lazy users to registered users.
    """
    def custom_signup(self, request, user):
        if is_lazy_user(request.user):
            lazy_user = request.user
            convert_lazy_user(lazy_user, user)


class OrderedListSerializer(serializers.ListSerializer):
    """Infers order attribute from the position of each instance in the list.
    """
    order_start = 0

    def validate(self, data):
        for i in range(len(data)):
            data[i]['order'] = self.order_start + i
        return data


class SettableListSerializer(serializers.ListSerializer):
    """Allows to set new instances for a domain manager.
    """
    def set(self, manager, initial_data):
        """Create or update instances of given manager according to data.
        Assumes not-validated initial_data.
        """
        data = self.validate(initial_data)
        instance_map = {
            instance.id: instance
            for instance in manager.model.objects.all()}
        current_instances = []
        for instance_data in data:
            instance = instance_map.get(instance_data['id'], None)
            serializer = self.child.__class__(instance=instance, data=instance_data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            current_instances.append(instance)
        manager.set(current_instances)
        return current_instances


class SettableOrderedListSerializer(SettableListSerializer, OrderedListSerializer):
    pass


class BlockSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()  # defined explicitly to make it writable
    name = serializers.SlugField(validators=[])
    order = serializers.IntegerField(default=int)

    class Meta:
        model = Block
        fields = ('id', 'name', 'order')
        list_serializer_class = SettableOrderedListSerializer


class ToolboxSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()  # defined explicitly to make it writable
    # Don't check uniqueness of name is needed to allow multiple update of
    # existing toolboxes.
    name = serializers.SlugField(validators=[])
    blocks = serializers.SlugRelatedField(
        slug_field='name',
        many=True,
        queryset=Block.objects.all())

    class Meta:
        model = Toolbox
        fields = ('id', 'name', 'blocks')
        list_serializer_class = SettableListSerializer


class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = ('id', 'name')


class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()  # defined explicitly to make it writable
    #level = serializers.SlugRelatedField(
    #    slug_field='name',
    #    many=False,
    #    queryset=Level.objects.all(),
    #    required=False)

    class Meta:
        model = Task
        fields = ('id', 'name', 'setting', 'solution')
        list_serializer_class = SettableListSerializer


class SettingSerializer(serializers.Serializer):
    toolbox = serializers.CharField(required=False)


class ChunkSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()  # defined explicitly to make it writable
    name = serializers.SlugField(validators=[])
    setting = SettingSerializer(required=False)
    tasks = serializers.SlugRelatedField(
        slug_field='name',
        many=True,
        queryset=Task.objects.all(),
        default=list)
    subchunks = serializers.SlugRelatedField(
        slug_field='name',
        many=True,
        queryset=Chunk.objects.all(),
        default=list)

    class Meta:
        model = Chunk
        fields = ('id', 'name', 'order', 'setting', 'tasks', 'subchunks')
        list_serializer_class = SettableOrderedListSerializer

    def create(self, validated_data):
        task_names = validated_data.pop('tasks', None)
        subchunk_names = validated_data.pop('subchunks', None)
        chunk = Chunk.objects.create(**validated_data)
        if task_names:
            tasks = [Task.objects.get(name=name) for name in task_names]
            chunk.tasks.set(tasks)
        if subchunk_names:
            subchunks = [Chunk.objects.get(name=name) for name in subchunk_names]
            chunk.subchunks.set(subchunks)
        return chunk

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.order = validated_data.get('order', instance.order)
        instance.setting = validated_data.get('setting', instance.setting)
        task_names = validated_data.pop('tasks', None)
        subchunk_names = validated_data.pop('subchunks', None)
        if task_names:
            tasks = [Task.objects.get(name=name) for name in task_names]
            instance.tasks.set(tasks)
        if subchunk_names:
            subchunks = [Chunk.objects.get(name=name) for name in subchunk_names]
            instance.subchunks.set(subchunks)
        instance.save()
        return instance


class MissionListSerializer(SettableOrderedListSerializer):
    order_start = 1


class MissionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()  # defined explicitly to make it writable
    name = serializers.SlugField(validators=[])
    chunk = serializers.SlugRelatedField(
        slug_field='name',
        many=False,
        queryset=Chunk.objects.all())

    class Meta:
        model = Mission
        fields = ('id', 'order', 'name', 'chunk')
        list_serializer_class = MissionListSerializer


class DomainSerializer(serializers.ModelSerializer):
    name = serializers.SlugField()
    blocks = BlockSerializer(many=True)
    toolboxes = ToolboxSerializer(many=True)
    tasks = TaskSerializer(many=True)
    chunks = ChunkSerializer(many=True)
    missions = MissionSerializer(many=True)

    class Meta:
        model = Domain
        fields = ('name', 'blocks', 'toolboxes', 'tasks', 'chunks', 'missions')

    def create_or_update(self, data):
        # Call directly without validation!
        domain, _created = Domain.objects.get_or_create(name=data['name'])
        BlockSerializer(many=True).set(domain.blocks, data['blocks'])
        ToolboxSerializer(many=True).set(domain.toolboxes, data['toolboxes'])
        TaskSerializer(many=True).set(domain.tasks, data['tasks'])
        ChunkSerializer(many=True).set(domain.chunks, data['chunks'])
        MissionSerializer(many=True).set(domain.missions, data['missions'])
        return domain


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
    classroom = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Classroom.objects.all())
    practice_overview = serializers.HyperlinkedIdentityField(
        view_name='student-practice-overview')
    start_task = serializers.HyperlinkedIdentityField(
        view_name='student-start-task')
    edit_program = serializers.HyperlinkedIdentityField(
        view_name='student-edit-program')
    run_program = serializers.HyperlinkedIdentityField(
        view_name='student-run-program')

    class Meta:
        model = Student
        fields = (
            'url', 'user', 'credits', 'level',
            'classroom', 'practice_overview',
            'start_task', 'edit_program', 'run_program')

    def get_level(self, student):
        domain = get_domain()
        level = get_level(domain, student)
        return level


class TaskSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSession
        fields = ('id', 'student', 'task', 'solved', 'start', 'end')
        read_only_fields = ('student', 'solved', 'start', 'end')
        # Student field is made read-only as it should be determined by the
        # current user and passed by TaskSessionsViewSet.perform_create().
        # Note that the serializer is currently not used (but will if we will
        # enable student to see history of their past attempts).


class StudentTaskSerializer(serializers.Serializer):
    name = serializers.CharField()
    attempted = serializers.BooleanField()
    solved = serializers.BooleanField()
    time = serializers.IntegerField()  # number of seconds


class StudentSkillSerializer(serializers.Serializer):
    name = serializers.CharField()
    value = serializers.FloatField()


class RecommendationSerializer(serializers.Serializer):
    available = serializers.BooleanField()
    task = serializers.CharField()
    phase = serializers.CharField()
    mission = serializers.CharField()


class PracticeOverviewSerializer(serializers.Serializer):
    level = serializers.IntegerField()
    mission = serializers.CharField()
    phase = serializers.CharField()
    credits = serializers.IntegerField()
    tasks = StudentTaskSerializer(many=True)
    skills = StudentSkillSerializer(many=True)
    recommendation = RecommendationSerializer()


class ProgressSerializer(serializers.Serializer):
    chunk = serializers.CharField()
    skill = serializers.FloatField()


class RunProgramResponseSerializer(serializers.Serializer):
    correct = serializers.BooleanField()
    progress = ProgressSerializer(required=False, many=True)
    recommendation = RecommendationSerializer(required=False)
