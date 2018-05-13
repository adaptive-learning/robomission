"""Parsing domain from source files.

Domain is specified by a json file with missions, chunks, tasks, toolboxes,
and blocks. Each task name points to a Markdown file which is assumed to be
in ./tasks/{name}.md path relative to the json file.

Current domain resides in //backend/domain/domain.json
"""
import json
import os
from django.conf import settings
from learn.models import Task, DomainParam, get_chunk, Chunk
from learn.serializers import DomainSerializer
from learn.utils import js


def load_domain_from_file(name='domain/domain.json'):
    path = os.path.join(settings.REPO_DIR, 'backend', name)
    with open(path) as infile:
        data = json.load(infile)
    task_dir = os.path.join(os.path.dirname(path), data['include']['tasks'])
    inject_tasks_data(data['tasks'], task_dir)
    # TODO: inject order?
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
        chunk = None
        chunk_name = param_data.pop('chunk', None)
        if chunk_name:
            try:
                chunk = get_chunk(chunk_name)
            except Chunk.DoesNotExist:
                print(
                    'Warning: Specified non-existing chunk "{0}". Skipping.'\
                    .format(chunk_name))
                continue
        for name, value in param_data.items():
            DomainParam.objects.update_or_create(
                domain=domain, chunk=chunk, name=name,
                defaults={'value': value})


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
    setting = data['setting']
    setting['fields'] = normalize_fields(setting['fields'])
    adapted_data = {
        'name': data['id'],
        'setting': setting,
        'solution': data['solution'],
    }
    return adapted_data

def normalize_fields(text):
    rows = text.strip().replace(' ', '').split('\n')
    fields = ';'.join(row.strip('|') for row in rows)
    return fields

# TODO: Remove if not needed.
#def fields_to_str(fields):
#    return '||'.join(row_to_str(row) for row in fields)
#
#
#def row_to_str(row):
#    return '|'.join(bg + ''.join(objects) for bg, objects in row)
