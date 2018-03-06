"""Utils for working with domain.
"""
import json
import os
from django.conf import settings
from learn.serializers import DomainSerializer
from learn.models import Task
from learn.utils import js
from learn.serializers import TaskSerializer


def load_domain_from_file(name='domain/domain.json'):
    path = os.path.join(settings.REPO_DIR, 'backend', name)
    with open(path) as infile:
        data = json.load(infile)
    task_dir = os.path.join(os.path.dirname(path), 'tasks')
    inject_tasks_data(data['tasks'], task_dir)
    serializer = DomainSerializer()
    domain = serializer.create_or_update(data)
    return domain


def inject_tasks_data(data, task_dir):
    for task_data in data:
        #task = Task.objects.filter(pk=task_data['id']).first()
        task_name = task_data['name']
        source = read_task_source(task_dir, task_name)
        source_data = parse_task_source(source)
        if task_name != source_data['name']:
            raise ValueError(
                "File name '{0}' doesn't match its headline '{1}'.".format(
                    task_name, source_data['name']))
        task_data.update(source_data)


def read_task_source(dirpath, name):
    path = task_name_to_path(dirpath, name)
    with open(path) as infile:
        content = infile.read()
    return content


def task_name_to_path(dirpath, name):
    return os.path.join(dirpath, name + '.md')


def parse_task_source(text):
    data = js.run_script(script_name='parseTask', input_text=text)
    # TODO: Remove level, and replace by chunk, once DB model and JS parsing
    # function is changed.
    # TODO: Use nested serialized for setting parsing.
    adapted_data = {
        'name': data['id'],
        # 'level': data['category'],
        'setting': json.dumps(data['setting']),
        'solution': data['solution'],
    }
    return adapted_data
