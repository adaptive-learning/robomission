"""Views and utilities for exporting data to csv.
"""
from django.conf import settings
from django.shortcuts import redirect
from rest_framework import permissions
from rest_framework import serializers
from rest_framework import viewsets
from rest_pandas import PandasSerializer, PandasViewSet
from learn.models import Block, Toolbox, Task, Chunk, Mission
from learn.models import TaskSession, ProgramSnapshot


class ExportViewSet(PandasViewSet):
    # Currently, the export API is only available to staff users, with the
    # exception of the already exported bundles, which are stored in the media
    # dir and are available to everybody with direct URL.
    # In the future, we might want to use the PandasViewSets with their
    # dataframes transformations to serve some portions of the data to users;
    # in such case, the permissions would need to rethink.
    permission_classes = (permissions.IsAdminUser,)

    def get_dataframe(self):
        queryset = self.filter_queryset(self.get_queryset())
        # The `with_list_serializer` method combines standard serializer class
        # with a Pandas serializer class. See:
        # https://github.com/wq/django-rest-pandas/blob/master/rest_pandas/views.py
        serializer_class = self.with_list_serializer(self.serializer_class)
        serializer = serializer_class(queryset, many=True)
        df = serializer.data
        return df


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ('id', 'name', 'order')


class BlockViewSet(ExportViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer


class ToolboxSerializer(serializers.ModelSerializer):
    blocks = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)

    class Meta:
        model = Toolbox
        fields = ('id', 'name', 'blocks')


class ToolboxViewSet(ExportViewSet):
    queryset = Toolbox.objects.all().prefetch_related('blocks')
    serializer_class = ToolboxSerializer


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name', 'setting', 'solution')


class TaskViewSet(ExportViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class ChunkSerializer(serializers.ModelSerializer):
    subchunks = serializers.SlugRelatedField(
        slug_field='name', many=True, read_only=True)
    tasks = serializers.SlugRelatedField(
        slug_field='name', many=True, read_only=True)
    class Meta:
        model = Chunk
        fields = ('id', 'name', 'order', 'setting', 'subchunks', 'tasks')


class ChunkViewSet(ExportViewSet):
    queryset = Chunk.objects.all()
    serializer_class = ChunkSerializer


class MissionSerializer(serializers.ModelSerializer):
    chunk = serializers.SlugRelatedField(
        slug_field='name', many=False, read_only=True)
    class Meta:
        model = Mission
        fields = ('id', 'name', 'order', 'chunk')


class MissionViewSet(ExportViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer


class TaskSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSession
        fields = ('id', 'student', 'task', 'solved', 'start', 'end', 'time_spent')


class TaskSessionsViewSet(ExportViewSet):
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


class ProgramSnapshotsViewSet(ExportViewSet):
    # Not only task session, but also its snapshots must be prefetched to avoid
    # generating individual SQL queries for each serialed row. (The reason is
    # in ProgramSnapshot.order which is a computed property and needs to know
    # all snapshots of its task session.)
    # TODO: Once the order is computed on save(), it is enought to
    # select_related('task_session') (that is still needed for time_from
    # start), although that could be computed on save() as well.
    queryset = ProgramSnapshot.objects.prefetch_related('task_session__snapshots').all()
    serializer_class = ProgramSnapshotSerializer
    pandas_serializer_class = ProgramSnapshotPandasSerializer


class LatestBundleViewSet(viewsets.ViewSet):
    """Phony ViewSet to specify a custom entry in the rest API.
    """
    # The already exported files are avaible to everybody with direct URL to
    # the media dir; e.g. the latest bundle can be downloaded by anybody at:
    # `http://robomise.cz/media/exports/robomission-latest.zip`.
    permission_classes = ()

    def list(self, request, format=None):
        bundle_url = '{media}exports/{bundle_name}'.format(
            media=settings.MEDIA_URL,
            bundle_name=settings.EXPORT_BUNDLE_NAME)
        return redirect(bundle_url)
