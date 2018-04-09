"""Parsing domain from source files.

Domain is specified by a json file with missions, chunks, tasks, toolboxes,
and blocks. Each task name points to a Markdown file which is assumed to be
in ./tasks/{name}.md path relative to the json file.

Current domain resides in //backend/domain/domain.json
"""
import json
import os
from django.conf import settings
from learn.models import Task, Chunk, DomainParam
from learn.serializers import DomainSerializer
from learn.utils import js


def load_domain_from_file(name='domain/domain.json'):
    path = os.path.join(settings.REPO_DIR, 'backend', name)
    with open(path) as infile:
        data = json.load(infile)
    task_dir = os.path.join(os.path.dirname(path), data['include']['tasks'])
    inject_tasks_data(data['tasks'], task_dir)
    serializer = DomainSerializer()
    domain = serializer.create_or_update(data)
    params_path = os.path.normpath(
        os.path.join(os.path.dirname(path), data['include']['params']))
    load_domain_params(domain, params_path)
    return domain


def load_domain_params(domain, params_path):
    print('Loading domain parameters from', params_path, '...')
    with open(params_path) as infile:
        data = json.load(infile)
    assert domain.name == data['domain']
    for param_data in data['params']:
        task_name = param_data.pop('task', None)
        task = Task.objects.filter(name=task_name).first()
        if task_name and not task:
            print('Warning: Specified non-existing task "{task}". Skipping.'\
                  .format(task=task_name))
            continue
        chunk_name = param_data.pop('chunk', None)
        chunk = Chunk.objects.filter(name=chunk_name).first()
        if chunk_name and not chunk:
            print('Warning: Specified non-existing chunk "{chunk}". Skipping.'\
                  .format(chunk=chunk_name))
            continue
        for name, value in param_data.items():
            DomainParam.objects.create(
                domain=domain, task=task, chunk=chunk, name=name, value=value)


def inject_tasks_data(data, task_dir):
    for task_data in data:
        #task = Task.objects.filter(pk=task_data['id']).first()
        task_name = task_data['name']
        print('Parsing task', task_name, '...')  # TODO:logging
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
