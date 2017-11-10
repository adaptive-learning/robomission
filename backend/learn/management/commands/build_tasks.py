from functools import singledispatch
import json
import os
import re
from subprocess import Popen, PIPE
from django.core.management.base import BaseCommand
from django.conf import settings
from learn.models import Task
from learn.serializers import TaskSerializer


class Command(BaseCommand):
    help = "Build tasks in //tasks directory and saves them to DB."

    def handle(self, *args, **options):
        self.stdout.write('Building tasks...')
        file_names = [
            name for name in os.listdir(settings.TASKS_DIR)
            if name.endswith('.md')]
        names = [file_name[:-3] for file_name in file_names]
        sources = [self.read_task_source(name) for name in names]
        for name, source in zip(names, sources):
            self.stdout.write('Building task: {}'.format(name))
            build_task_from_source(source)
        self.stdout.write(self.style.SUCCESS('{n} tasks built.'.format(n=len(sources))))

    def read_task_source(self, name):
        path = task_name_to_path(name)
        self.stdout.write('Reading source: {}'.format(path))
        with open(path) as infile:
            content = infile.read()
        return content


def task_name_to_path(name):
    return os.path.join(settings.TASKS_DIR, name + '.md')


def build_task_from_source(text):
    data = run_js_script(script_name='parseTask', input_text=text)
    # TODO: remove adapting bellow when category is changed to level on frontend
    # and TaskSerializer correctly handles json data
    name = data['id']
    adapted_data = {
        'name': name,
        'level': data['category'],
        'setting': json.dumps(data['setting']),
        'solution': json.dumps(data['solution']),
    }
    if Task.objects.filter(name=name).exists():
        task = Task.objects.get(name=name)
        task_serializer = TaskSerializer(task, data=adapted_data)
    else:
        task_serializer = TaskSerializer(data=adapted_data)
    task_serializer.is_valid(raise_exception=True)
    #print(task_serializer.validated_data)
    task_serializer.save()



def run_js_script(script_name, input_text):
    # TODO: better error handling
    path = os.path.join(settings.JS_TOOLS_DIR, script_name)
    with Popen([settings.JS_NODE_PATH, path], stdout=PIPE, stdin=PIPE, stderr=PIPE) as js_process:
        enc_stdout, enc_stderr = js_process.communicate(input=input_text.encode())
    stdout = enc_stdout.decode()
    stderr = enc_stderr.decode()
    if stderr:
        raise ValueError('Running JS script {name} failed.\n{description}'.format(
            name=script_name, description=create_description(input_text, stdout, stderr)))
    #result = camel_to_snake_case(json.loads(stdout))
    result = json.loads(stdout)
    return result


def create_description(input_text, stdout, stderr):
    description = '\n'.join([
        '##### input: #####', input_text,
        '##### output: #####', stdout,
        '##### error: #####', stderr,
        '##########'
    ])
    return description


@singledispatch
def camel_to_snake_case(name):
    partially_underscored = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    fully_underscored = re.sub('([a-z0-9])([A-Z])', r'\1_\2', partially_underscored)
    return fully_underscored.lower()


@camel_to_snake_case.register(dict)
def _camel_to_snake_case(mapping):
    return {camel_to_snake_case(key): value for key, value in mapping.items()}
