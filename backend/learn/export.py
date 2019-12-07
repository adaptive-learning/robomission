"""Views and utilities for exporting data to csv.
"""
from collections import OrderedDict
import csv
from functools import partial
import json
import os
from django.conf import settings
from django.shortcuts import redirect
import numpy as np
import pandas as pd
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

    def export_to_csv(self, path):
        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            fields = tuple(self.serializer_class().fields.keys())
            writer.writerow(fields)
            for entity in self.queryset:
                row = tuple(self.serializer_class(entity).data.values())
                writer.writerow(row)


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



# Memory and time optimized export of all entities.
def export_to_csv(path):
    problems = make_problems_df()
    events = make_events_df()
    attempts = make_attempts_df(events, problems)

    # Remove auxiliary columns.
    events = events.drop('_attempt_start', axis=1)
    # Save the DataFrames.
    events.to_csv(os.path.join(path, 'events.csv'))
    attempts.to_csv(os.path.join(path, 'attempts.csv'))
    problems.to_csv(os.path.join(path, 'problems.csv'))


def make_problems_df():
    problems = pd.DataFrame.from_records(TaskViewSet.queryset.values())
    ps = make_problemset_df()
    problems = problems.apply(partial(prepare_problem, ps=ps), axis=1)
    problems = problems.set_index('id')
    problems = problems.sort_values(by=['level1', 'level2', 'level3'])
    return problems


def make_problemset_df():
    ps = pd.DataFrame.from_records(ProblemSetViewSet.queryset.values())
    ps['content'] = ps['content'].apply(json.loads)
    ps = ps.set_index('id')
    return ps


def prepare_problem(record, ps):
    content = json.loads(record.content)
    problem = pd.Series(OrderedDict([
        ('id', record.id),
        ('name', record['name']),
        ('statement', aggregate_problem_statement(record, ps)),
        ('context', aggregate_problem_context(record, ps)),
        ('solution', content['solution']),
        ('problemset', 3 * (record['level'] - 1) + record.level2),
        ('section', '{}.{}.{}'.format(record['level'], record.level2, record.level3)),
        ('level1', record['level']),
        ('level2', record.level2),
        ('level3', record.level3),
    ]))
    return problem


def aggregate_problem_statement(record, ps):
    content = json.loads(record.content)
    phase = ps.loc[record.problemset_id]
    phase_setting = phase.content['setting']
    mission = ps.loc[phase.parent_id]
    mission_setting = mission.content['setting']
    statement = {**mission_setting, **phase_setting, **content['setting']}
    statement['toolbox'] = get_toolbox_as_blocks(statement['toolbox'])
    return statement


def aggregate_problem_context(record, ps):
    phase = ps.loc[record.problemset_id]
    mission = ps.loc[phase.parent_id]
    context = {
        'ordering': [record['level'], record.level2, record.level3],
        'mission_name': mission['name'],
        'problemset_name': phase['name'],
    }
    return context


def make_events_df():
    attempts = pd.DataFrame.from_records(TaskSessionsViewSet.queryset.values())
    attempts = pd.DataFrame({
        'id': attempts.id,
        'attempt_start': attempts.start,
        'student': attempts.student_id,
        'problem': attempts.task_id,
    })
    attempts = attempts.set_index('id')
    events = pd.DataFrame.from_records(ProgramSnapshotsViewSet.queryset.values())
    events = events.join(attempts, on='task_session_id')
    events = pd.DataFrame(OrderedDict([
        ('id', events.id),
        ('event_order', events.time.rank(method='first').astype(int)),
        ('timestamp', events.time),
        ('event_type', events.granularity),
        ('student', events.student),
        ('problem', events.problem),
        ('attempt', events.task_session_id),
        # Make minicode characters unambiguous.
        ('program', events.program.fillna('').str.replace('r{', 'd{')),
        ('correct', events.correct),
        ('time_from_attempt_start', events.time_from_start),
        ('tools', 'robomission:1.0'),
        ('_attempt_start', events.attempt_start),  # used for attempts aggregation
    ]))
    events = events.set_index('id')
    events = events.sort_values('event_order')
    # Hack to denote the old code version.
    is_new_version = events.timestamp < '2018-05-26'
    events['tools'] = events['tools'].where(is_new_version, other='robomission:1.1')
    # Remove incorrectly matched one-step-forward attempts.
    events = events[(events.problem != 51) | (events.tools != 'robomission:1.0')]
    # Renumber.
    events['event_order'] = events['event_order'].rank(method='first').astype(int)
    return events


def make_attempts_df(events, problems):
    """Prepare attempts by grouping the events.
    (Automatically ignoring the # attempts without any event.)
    """
    # TODO: Aggregate by custom rules based on the delay between events.
    attempts = events.groupby('attempt').apply(aggregate_events_of_single_attempt)
    attempts.index.rename('id', inplace=True)
    attempts = attempts.sort_values('start')
    # TODO: Explore and discuss which problems' fields are so frequently used
    # that it's better to join them to the attempts df.
    problem_columns = ['problemset']
    attempts = attempts.join(problems[problem_columns], on='problem')
    return attempts


def aggregate_events_of_single_attempt(events):
    solved = events.correct.max() == 1
    n_events = len(events)
    n_edits = np.sum(events.event_type == 'edit')
    n_executions = np.sum(events.event_type == 'execution')
    # TODO: Make sure not to count the events after the first correct submit.
    # (They are currently not logged in RoboMission.)
    first_event = events.iloc[0]
    last_event = events.iloc[n_events - 1]
    time = last_event.time_from_attempt_start
    program = last_event.program
    return pd.Series(OrderedDict([
        ('student', first_event.student),
        ('problem', first_event.problem),
        ('start', first_event['_attempt_start']),
        ('solved', solved),
        ('time', time),
        ('n_edits', n_edits),
        ('n_executions', n_executions),
        ('program', program),
        #('programs', list(events.program))
    ]))


def get_toolbox_as_blocks(name):
    # TODO" Use the toolboxes defined in the domain to ensure consistency.
    TOOLBOXES = {
        'fly': ['fly'],
        'shoot': ['fly', 'shoot'],
        'repeat': ['fly', 'shoot', 'repeat'],
        'while': ['fly', 'shoot', 'while', 'color'],
        'loops': ['fly', 'shoot', 'repeat', 'while', 'color'],
        'loops-if': ['fly', 'shoot', 'repeat', 'while', 'color', 'if'],
        'loops-if-position': ['fly', 'shoot', 'repeat', 'while', 'color', 'position', 'if'],
        'loops-if-else': ['fly', 'shoot', 'repeat', 'while', 'color', 'position', 'if', 'if-else']
    }
    return TOOLBOXES[name]
