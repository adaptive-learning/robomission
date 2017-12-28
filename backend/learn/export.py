"""Views and utilities for exporting data to csv.
"""
from django.conf import settings
from django.shortcuts import redirect
from rest_framework import serializers
from rest_framework import viewsets
from rest_pandas import PandasSerializer, PandasViewSet
from learn.models import Block, Toolbox, Level, Task, Instruction
from learn.models import Action, Student, TaskSession, ProgramSnapshot


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ('id', 'name', 'order')


class BlockViewSet(PandasViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer


class ToolboxSerializer(serializers.ModelSerializer):
    blocks = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)

    class Meta:
        model = Toolbox
        fields = ('id', 'name', 'blocks')


class ToolboxViewSet(PandasViewSet):
    queryset = Toolbox.objects.all().prefetch_related('blocks')
    serializer_class = ToolboxSerializer


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


class LevelViewSet(PandasViewSet):
    queryset = Level.objects.all().select_related('toolbox').prefetch_related('tasks')
    serializer_class = LevelSerializer


class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = ('id', 'name')


class InstructionViewSet(PandasViewSet):
    serializer_class = InstructionSerializer
    queryset = Instruction.objects.all()


class TaskSerializer(serializers.ModelSerializer):
    level = serializers.SlugRelatedField(
        slug_field='name',
        many=False,
        queryset=Level.objects.all())

    class Meta:
        model = Task
        fields = ('id', 'name', 'level', 'setting', 'solution')


class TaskViewSet(PandasViewSet):
    queryset = Task.objects.all().select_related('level')
    serializer_class = TaskSerializer


class StudentSerializer(serializers.ModelSerializer):
    credits = serializers.IntegerField(read_only=True)
    seen_instructions = serializers.SlugRelatedField(
        slug_field='name',
        many=True,
        read_only=True)

    class Meta:
        model = Student
        fields = ('id', 'credits', 'seen_instructions')


class StudentViewSet(PandasViewSet):
    queryset = Student.objects.prefetch_related('seen_instructions').all()
    serializer_class = StudentSerializer


class TaskSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSession
        fields = ('id', 'student', 'task', 'solved', 'start', 'end', 'time_spent')


class TaskSessionsViewSet(PandasViewSet):
    queryset = TaskSession.objects.all()
    serializer_class = TaskSessionSerializer


class ProgramSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramSnapshot
        fields = (
            'id', 'task_session', 'time', 'program',
            'granularity', 'order', 'correct', 'time_from_start')


def to_delta(times):
    deltas = times.diff()
    deltas.iat[0] = times.iat[0]
    return deltas


class ProgramSnapshotPandasSerializer(PandasSerializer):
    def transform_dataframe(self, dataframe):
        """Add a column with time since last snapshot of the same granularity.
        """
        grouped_programs = dataframe.groupby(['task_session', 'granularity'])
        dataframe['time_delta'] = grouped_programs.time_from_start.transform(to_delta)
        return dataframe


class ProgramSnapshotsViewSet(PandasViewSet):
    queryset = ProgramSnapshot.objects.select_related('task_session').all()
    serializer_class = ProgramSnapshotSerializer
    pandas_serializer_class = ProgramSnapshotPandasSerializer


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ('id', 'name', 'student', 'task', 'time', 'randomness', 'data')


class ActionsViewSet(PandasViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer


class LatestBundleViewSet(viewsets.ViewSet):
    """Phony ViewSet to specify a custom entry in the rest API.
    """
    # DRF can't derive DjangoModelPermissions for ViewSets without a queryset,
    # so we need to explicitly define them.
    permission_classes = ()

    def list(self, request, format=None):
        bundle_url = '{media}exports/{bundle_name}'.format(
            media=settings.MEDIA_URL,
            bundle_name=settings.EXPORT_BUNDLE_NAME)
        return redirect(bundle_url)
