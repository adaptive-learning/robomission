from django.contrib.auth import login
from django.contrib.auth.models import User
from lazysignup.utils import is_lazy_user
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from learn.credits import get_active_credits, get_level_value
from learn.models import Block, Toolbox, Level, Task, Instruction
from learn.models import Action, ProgramSnapshot, Student, TaskSession
from learn.models import Teacher, Classroom
from learn.models import Chunk, Mission, Domain
from learn.users import convert_lazy_user, is_initial_user
from learn.world import get_world


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


class CompleteUpdateListSerializer(serializers.ListSerializer):
    """All existing entities not specified in the list are removed.
    """
    model = None

    def create(self, validated_data):
        return self.update(self.model.objects.all(), validated_data)

    def update(self, instance, validated_data):
        entity_map = {entity.id: entity for entity in instance}
        current_entities = []
        for data in validated_data:
            entity = entity_map.get(data['id'], None)
            if entity is None:
                current_entities.append(self.child.create(data))
            else:
                current_entities.append(self.child.update(entity, data))
        # Remove old entitys not specified in the provided data.
        current_entity_ids = {data['id'] for data in validated_data}
        for entity_id, entity in entity_map.items():
            if entity_id not in current_entity_ids:
                entity.delete()
        return current_entities


class BlockListSerializer(CompleteUpdateListSerializer, OrderedListSerializer):
    model = Block


class BlockSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()  # defined explicitly to make it writable
    name = serializers.SlugField(validators=[])
    order = serializers.IntegerField(default=int)

    class Meta:
        model = Block
        fields = ('id', 'name', 'order')
        list_serializer_class = BlockListSerializer


class ToolboxListSerializer(CompleteUpdateListSerializer):
    model = Toolbox


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
        list_serializer_class = ToolboxListSerializer


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
        fields = ('id', 'level', 'name', 'credits', 'toolbox', 'tasks')


class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = ('id', 'name')


class TaskSerializer(serializers.ModelSerializer):
    level = serializers.SlugRelatedField(
        slug_field='name',
        many=False,
        queryset=Level.objects.all())

    class Meta:
        model = Task
        fields = ('id', 'name', 'level', 'setting', 'solution')


class SettingSerializer(serializers.Serializer):
    toolbox = serializers.CharField(required=False)


class ChunkListSerializer(CompleteUpdateListSerializer, OrderedListSerializer):
    model = Chunk


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
        list_serializer_class = ChunkListSerializer

    def create(self, validated_data):
        tasks = validated_data.pop('tasks')
        chunk = Chunk.objects.create(**validated_data)
        for task_name in tasks:
            task = Task.objects.get(name=task_name)
            chunk.tasks.add(task)
        return chunk

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.order = validated_data.get('order', instance.order)
        instance.setting = validated_data.get('setting', instance.setting)
        if 'tasks' in validated_data:
            task_names = validated_data.pop('tasks')
            tasks = [Task.objects.get(name=name) for name in task_names]
            instance.tasks.set(tasks)
        if 'subchunks' in validated_data:
            subchunk_names = validated_data.pop('subchunks')
            subchunks = [Chunk.objects.get(name=name) for name in subchunk_names]
            instance.subchunks.set(subchunks)
        instance.save()
        return instance


class MissionListSerializer(CompleteUpdateListSerializer, OrderedListSerializer):
    order_start = 1
    model = Mission


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
    #toolboxes = ToolboxSerializer(many=True, validators=[])
    toolboxes = ToolboxSerializer(many=True)
    tasks = TaskSerializer(many=True)
    chunks = ChunkSerializer(many=True)
    missions = MissionSerializer(many=True)

    def validate_blocks(self, data):
        serializer = BlockSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        instances = serializer.save()
        return instances

    def validate_toolboxes(self, data):
        serializer = ToolboxSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        instances = serializer.save()
        return instances

    def validate_tasks(self, data):
        serializer = TaskSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        instances = serializer.save()
        return instances

    def validate_chunks(self, data):
        serializer = ChunkSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        instances = serializer.save()
        return instances

    def validate_missions(self, data):
        serializer = MissionSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        instances = serializer.save()
        return instances

    class Meta:
        model = Domain
        fields = ('name', 'blocks', 'toolboxes', 'tasks', 'chunks', 'missions')
        #validators = []
        #extra_kwargs = {
        #    'toolboxes': {'validators': []}
        #}

    def create(self, validated_data):
        domain = Domain.objects.create(name=validated_data['name'])
        domain.blocks.set(validated_data['blocks'])
        domain.toolboxes.set(validated_data['toolboxes'])
        domain.tasks.set(validated_data['tasks'])
        domain.chunks.set(validated_data['chunks'])
        domain.missions.set(validated_data['missions'])
        return domain

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        instance.blocks.set(validated_data['blocks'])
        instance.toolboxes.set(validated_data['toolboxes'])
        instance.tasks.set(validated_data['tasks'])
        instance.chunks.set(validated_data['chunks'])
        instance.missions.set(validated_data['missions'])
        return instance


# Deprecated.
# TODO: Replace all its usage by DomainSerializer, then remove.
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
            'url', 'user', 'credits', 'level', 'active_credits',
            'seen_instructions', 'classroom', 'practice_overview',
            'start_task', 'watch_instruction', 'edit_program', 'run_program')

    def get_active_credits(self, student):
        world = get_world()
        return get_active_credits(world, student)

    def get_level(self, student):
        world = get_world()
        return get_level_value(world, student)


class TaskSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSession
        fields = ('id', 'student', 'task', 'solved', 'start', 'end')
        read_only_fields = ('student', 'solved', 'start', 'end')
        # Student field is made read-only as it should be determined by the
        # current user and passed by TaskSessionsViewSet.perform_create().
        # Note that the serializer is currently not used (but will if we will
        # enable student to see history of their past attempts).


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
