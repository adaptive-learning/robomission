"""Views and utilities for exporting data to csv.
"""
import csv
from django.conf import settings
from django.shortcuts import redirect
from rest_framework import permissions
from rest_framework import serializers
from rest_framework import viewsets
from rest_pandas import PandasViewSet
from learn.models import Block, Toolbox, Task, ProblemSet
from learn.models import TaskSession, ProgramSnapshot


class ExportViewSet(PandasViewSet):
    # Currently, the export API is only available to staff users, with the
    # exception of the already exported bundles, which are stored in the media
    # dir and are available to everybody with direct URL.
    # In the future, we might want to use the PandasViewSets with their
    # dataframes transformations to serve some portions of the data to users;
    # in such case, the permissions would need to rethink.
    permission_classes = (permissions.IsAdminUser,)

    # Currently not used, but we may need it again once we introduce online
    # export of the latest data.
    def get_dataframe(self):
        queryset = self.filter_queryset(self.get_queryset())
        # The `with_list_serializer` method combines standard serializer class
        # with a Pandas serializer class. See:
        # https://github.com/wq/django-rest-pandas/blob/master/rest_pandas/views.py
        serializer_class = self.with_list_serializer(self.serializer_class)
        serializer = serializer_class(queryset, many=True)
        df = serializer.data
        return df


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'id', 'name', 'setting', 'solution',
            'section', 'level', 'level2', 'order', 'mission', 'problemset')
        # Django Rest Pandas cannot derive itself that id field should be
        # index (related to the multitable inheritance).
        pandas_index = ['id']


class TaskViewSet(ExportViewSet):
    queryset = Task.objects.select_related('problemset__parent').all()
    serializer_class = TaskSerializer


class ProblemSetSerializer(serializers.ModelSerializer):
    parts = serializers.SlugRelatedField(
        slug_field='name', many=True, read_only=True)
    tasks = serializers.SlugRelatedField(
        slug_field='name', many=True, read_only=True)
    class Meta:
        model = ProblemSet
        fields = ('id', 'name',
                  'granularity', 'section', 'level', 'order',
                  'parent', 'n_parts', 'n_tasks',
                  'setting', 'parts', 'tasks')
        # Django Rest Pandas cannot derive itself that id field should be
        # index (related to the multitable inheritance).
        pandas_index = ['id']


class ProblemSetViewSet(ExportViewSet):
    queryset = (
        ProblemSet.objects
        .select_related('parent')
        .prefetch_related('parts', 'tasks')
        .all())
    serializer_class = ProblemSetSerializer


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
            'granularity', 'order', 'correct', 'time_from_start', 'time_delta')


class ProgramSnapshotsViewSet(ExportViewSet):
    queryset = ProgramSnapshot.objects.all()
    serializer_class = ProgramSnapshotSerializer


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


def save_viewset_to_csv(viewset, path):
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        fields = tuple(viewset.serializer_class().fields.keys())
        writer.writerow(fields)
        for entity in viewset.queryset:
            row = tuple(viewset.serializer_class(entity).data.values())
            writer.writerow(row)
